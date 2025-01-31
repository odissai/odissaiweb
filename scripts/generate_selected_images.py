import os
import json
import logging
from datetime import datetime
import time
from dotenv import load_dotenv
from generate_solution_images import SOLUTIONS, generate_image

CONFIG_FILE = "scripts/solutions_config.json"

def create_directories():
    """Create necessary directories for storing generated images"""
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    generation_dir = os.path.join("scripts", "generations", date_str)
    os.makedirs(generation_dir, exist_ok=True)
    
    assets_dir = os.path.join("scripts", "assets", "images", "solutions")
    os.makedirs(assets_dir, exist_ok=True)
    
    return generation_dir, assets_dir

def load_config():
    """Load the configuration file"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {
            "solutions_to_regenerate": [],
            "last_generation": None,
            "generation_history": []
        }
    except Exception as e:
        logging.error(f"Error loading config file: {str(e)}")
        return None

def update_config(config, generation_dir):
    """Update the configuration file with new generation information"""
    try:
        config["last_generation"] = datetime.now().isoformat()
        config["solutions_to_regenerate"] = []  # Clear the list after generation
        config["generation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "directory": generation_dir
        })
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        logging.error(f"Error updating config file: {str(e)}")

def main():
    """Main function to generate images for selected solutions"""
    # Ensure generations directory exists for log file
    os.makedirs(os.path.join("scripts", "generations"), exist_ok=True)
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join("scripts", "generations", "generation.log"), encoding='utf-8')
        ]
    )

    # Load environment variables
    try:
        load_dotenv(verbose=True)
        if "REPLICATE_API_TOKEN" not in os.environ:
            logging.error("REPLICATE_API_TOKEN environment variable is not set")
            return
        logging.info(f"API token found: {os.environ['REPLICATE_API_TOKEN'][:8]}...")
    except Exception as e:
        logging.error(f"Error loading environment: {str(e)}")
        return

    try:
        # Load configuration
        config = load_config()
        if config is None:
            logging.error("Failed to load configuration")
            return

        # Get solutions to regenerate
        solutions_to_regenerate = config.get("solutions_to_regenerate", [])
        if not solutions_to_regenerate:
            logging.info("No solutions marked for regeneration in config")
            return

        # Create directories
        generation_dir, assets_dir = create_directories()
        logging.info(f"Created directories: Generation={generation_dir}, Assets={assets_dir}")
        
        # Initialize summary data
        summary_data = {}
        
        # Process selected solutions
        for solution_id in solutions_to_regenerate:
            if solution_id not in SOLUTIONS:
                logging.warning(f"Unknown solution ID in config: {solution_id}")
                continue

            solution_data = SOLUTIONS[solution_id]
            logging.info(f"\nProcessing {solution_data['name']}...")
            
            image_url, local_path = generate_image(
                solution_data['prompt'],
                solution_id,
                generation_dir,
                assets_dir
            )
            
            if image_url and local_path:
                logging.info(f"Successfully generated and downloaded image for {solution_id}")
                summary_data[solution_id] = {
                    "name": solution_data['name'],
                    "url": image_url,
                    "local_path": local_path
                }
            else:
                logging.error(f"Failed to generate or download image for {solution_id}")
                
            # Add a small delay between generations and log progress
            total_solutions = len(solutions_to_regenerate)
            current_solution = solutions_to_regenerate.index(solution_id) + 1
            logging.info(f"Progress: {current_solution}/{total_solutions} solutions processed")
            if current_solution < total_solutions:
                delay = 5
                logging.info(f"Waiting {delay} seconds before next generation...")
                time.sleep(5)
        
        # Save summary
        summary_path = os.path.join(generation_dir, "summary.json")
        with open(summary_path, "w", encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        # Update config with generation information
        update_config(config, generation_dir)
        
        # Log final statistics
        successful = len([s for s in summary_data.values() if s.get('local_path')])
        total = len(solutions_to_regenerate)
        logging.info(f"\nGeneration complete. Successfully generated {successful}/{total} images.")
        logging.info(f"Summary saved to {summary_path}")
        
    except Exception as e:
        logging.error(f"Main execution error: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("\nGeneration interrupted by user")
        print("\nGeneration interrupted by user")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())