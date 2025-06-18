import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from logging import INFO

from dotenv import load_dotenv

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF

#################################################
# CONFIGURATION
#################################################
# Set up logging and environment variables for
# connecting to Neo4j database
#################################################
load_dotenv()


# Configure logging
logging.basicConfig(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

# Neo4j connection parameters
# Make sure Neo4j Desktop is running with a local DBMS started
neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')
neo4j_password = os.environ.get('NEO4J_PASSWORD', 'password')

if not neo4j_uri or not neo4j_user or not neo4j_password:
    raise ValueError('NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD must be set')

file_path = 'episodes.json'


async def main():
    #################################################
    # LOAD EPISODES.JSON
    #################################################
    episodes = None  # Initialize to None or an empty list/dict
    try:
        with open(file_path, 'r') as f:
            episodes = json.load(f)
        logger.info(f"Successfully loaded data from {file_path}.")
        # You can optionally print or log the data here if needed for verification:
        # logger.info(json.dumps(episodes, indent=4))
    except FileNotFoundError:
        logger.error(f"Error: The file {file_path} was not found.")
        # Decide how to handle this: raise error, exit, or continue with empty data
        return  # Or raise
    except json.JSONDecodeError:
        logger.error(f"Error: The file {file_path} contains invalid JSON.")
        # Decide how to handle this
        return  # Or raise
    except Exception as e:
        logger.error(
            f"An unexpected error occurred while reading {file_path}: {e}")
        return  # Or raise

    #################################################
    # INITIALIZATION
    #################################################
    # Connect to Neo4j and set up Graphiti indices
    # This is required before using other Graphiti
    # functionality
    #################################################

    # Initialize Graphiti with Neo4j connection
    graphiti = Graphiti(neo4j_uri, neo4j_user, neo4j_password)

    try:
        # Initialize the graph database with graphiti's indices. This only needs to be done once.
        await graphiti.build_indices_and_constraints()
        logger.info("Graphiti indices and constraints built successfully.")

        if episodes:
            logger.info(f"Adding {len(episodes)} episodes to Graphiti...")
            for i, episode_data in enumerate(episodes):
                try:
                    episode_name = episode_data.get('name')
                    if not episode_name:
                        logger.warning(
                            f"Episode {i} is missing 'name'. Using a placeholder name.")
                        episode_name = f"Unnamed Episode {i}"

                    episode_content = episode_data.get('content')
                    if episode_content is None:
                        logger.warning(
                            f"Episode '{episode_name}' is missing 'content'. Skipping.")
                        continue

                    episode_source_type_str = episode_data.get('type')
                    if not episode_source_type_str:
                        logger.warning(
                            f"Episode '{episode_name}' is missing 'type'. Skipping.")
                        continue

                    source_enum = None
                    try:
                        # Attempt direct mapping (e.g., "text" -> EpisodeType.TEXT if enum values are lowercase strings)
                        source_enum = EpisodeType(episode_source_type_str)
                    except ValueError:
                        # Attempt mapping by uppercase name (e.g., "TEXT" -> EpisodeType.TEXT if enum names are uppercase)
                        try:
                            source_enum = EpisodeType[episode_source_type_str.upper(
                            )]
                        except KeyError:
                            logger.error(
                                f"Episode '{episode_name}' has an unknown 'type': {episode_source_type_str}. Skipping.")
                            continue

                    # Default to empty string if missing
                    episode_description = episode_data.get('description', '')

                    await graphiti.add_episode(
                        name=episode_name,
                        episode_body=episode_content
                        if isinstance(episode_content, str)
                        else json.dumps(episode_content),
                        source=source_enum,
                        source_description=episode_description,
                        reference_time=datetime.now(timezone.utc),
                    )
                    logger.info(
                        f"Added episode: {episode_name} (Type: {source_enum.value})")
                except Exception as e_add_episode:
                    # Log error for this specific episode and continue with the next
                    current_episode_name = episode_data.get(
                        'name', f'Episode {i}')  # Get name again for error message
                    logger.error(
                        f"Failed to add episode '{current_episode_name}': {e_add_episode}")
            logger.info("Finished processing all episodes.")
        else:
            logger.warning(
                "No episodes found or loaded. Skipping episode addition to Graphiti.")
    except Exception as e:
        logger.error(
            f'An error occurred during Graphiti initialization or episode processing: {e}')
    finally:
        #################################################
        # CLEANUP
        #################################################
        # Always close the connection to Neo4j when
        # finished to properly release resources
        #################################################

        # Close the connection
        await graphiti.close()
        logger.info('\nConnection closed')

if __name__ == '__main__':
    asyncio.run(main())
