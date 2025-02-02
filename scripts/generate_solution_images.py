import os
import replicate
from datetime import datetime
import json
import logging
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse
import time

# Configuration
SOLUTIONS = {
    "formation": {
        "prompt": "Professional training room with ancient Greek android AI teachers in togas and laurel wreaths instructing humans, like Ulysses teaching his crew to resist the Sirens' song, knowledge represented as ethereal musical notes, mythological elements blended with modern technology, bright engaging atmosphere with Mediterranean sea in background, marble-textured androids with glowing circuit patterns", 
        "name": "Formation des Équipes"
    },
    "agents": {
        "prompt": "AI agents as ancient Greek marble-textured androids with glowing circuit patterns working with office software, visualization with Ulysses' ship navigating between Scylla's six heads and Charybdis' whirlpool represented as data streams, android assistants wearing togas and laurel wreaths avoiding digital monsters, clean professional style with Mediterranean sea colors",
        "name": "Agents IA sur Mesure"
    },
    "applications": {
        "prompt": "Fast AI development through Antikythera-like mechanism, ancient Greek android developers in togas with glowing circuit patterns inscribing code on marble tablets, on Circe's island where men were transformed to pigs, showing transformation of data, with Ithaca's azure blue waters and terracotta, Ulysses' ship sailing through lines of code", 
        "name": "Applications IA Rapides"
    },
    "conseil": {
        "prompt": "Strategic AI consulting with Greek philosopher androids in marble-textured bodies and glowing circuit patterns, in Calypso's grotto with modern office elements, ancient android advisors in togas analyzing sea charts like Ulysses outsmarting the one-eyed Cyclops Polyphemus, showing strategic vision and clever problem-solving",
        "name": "Conseil en Transformation IA"
    },
    "hebergement": {
        "prompt": "Secure AI hosting in Mount Olympus cloud infrastructure with temple servers, cybersecurity represented as android Poseidon with marble texture and glowing circuits commanding storms to protect data like Ulysses protecting his fleet from the Laestrygonian giants' attack, technical classical architecture with stormy seas and flying boulders",
        "name": "Hébergement Sécurisé"
    },
    "renforcement": {
        "prompt": "AI experts as Greek android mentors with marble texture and glowing circuit patterns in ancient library of King Alcinous, digital scrolls showing Ulysses' journey as learning paths, android scholars in togas working with Phaeacian ship builders, team overcoming challenges like Ulysses' crew passing the Wandering Rocks, Hellenistic art style with maritime elements",
        "name": "Renforcement des Équipes"
    }
}

def create_workflow_json(prompt):
    """Create the workflow JSON with the given prompt"""
    return {
        "1": {
            "inputs": {
                "text": prompt + ", Ghibli art style, ancient Greek theme, highly detailed, 8k resolution, masterpiece", 
                "clip": ["2", 1]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "CLIP Text Encode (Prompt)"}
        },
        "2": {
            "inputs": {"ckpt_name": "SDXL-Flash.safetensors"},
            "class_type": "CheckpointLoaderSimple",
            "_meta": {"title": "Load Checkpoint"}
        },
        "3": {
            "inputs": {
                "width": 768,
                "height": 1024, 
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage",
            "_meta": {"title": "Empty Latent Image"}
        },
        "4": {
            "inputs": {
                "seed": 156680208700286,
                "steps": 20,
                "cfg": 7,
                "sampler_name": "dpmpp_2m_sde",
                "scheduler": "karras", 
                "denoise": 1,
                "model": ["2", 0],
                "positive": ["1", 0],
                "negative": ["5", 0],
                "latent_image": ["3", 0]
            },
            "class_type": "KSampler",
            "_meta": {"title": "KSampler"}
        },
        "5": {
            "inputs": {
                "text": "text, watermark, blur, low quality, bad anatomy, bad hands, cropped, worst quality",
                "clip": ["2", 1]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "CLIP Text Encode (Prompt)"}
        },
        "6": {
            "inputs": {
                "samples": ["4", 0],
                "vae": ["2", 2]
            },
            "class_type": "VAEDecode",
            "_meta": {"title": "VAE Decode"}
        }
    }

def create_directories():
    """Create necessary directories for storing generated images"""
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    generation_dir = os.path.join("scripts", "generations", date_str)
    os.makedirs(generation_dir, exist_ok=True)
    
    assets_dir = os.path.join("scripts", "assets", "images", "solutions")
    os.makedirs(assets_dir, exist_ok=True)
    
    return generation_dir, assets_dir

def download_image(url, solution_id, assets_dir, generation_dir):
    """Download image from URL and save it locally"""
    try:
        logging.info(f"Downloading image from {url}")
        
        # Add retries for robustness
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                break
            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                if attempt == max_retries - 1:
                    raise
                logging.warning(f"Download attempt {attempt + 1} failed: {str(e)}. Retrying...")
                time.sleep(2)
        
        # Get file extension from URL or default to .webp
        path = urlparse(url).path
        ext = os.path.splitext(path)[1] or '.webp'
        
        # Create local file paths
        filename = f"{solution_id}{ext}"
        assets_filepath = os.path.join(assets_dir, filename)
        generation_filepath = os.path.join(generation_dir, filename)
        
        # Get image content
        image_content = response.content
        
        # Save the image in both directories
        for filepath in [assets_filepath, generation_filepath]:
            try:
                with open(filepath, 'wb') as f:
                    f.write(image_content)
                
                # Verify file was created and has content
                if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                    logging.info(f"Image successfully saved to {filepath}")
                else:
                    logging.error(f"Failed to save image or file is empty: {filepath}")
                    return None
            except IOError as e:
                logging.error(f"IOError while saving image to {filepath}: {str(e)}")
                return None
        
        return assets_filepath
            
    except Exception as e:
        logging.error(f"Error downloading image: {str(e)}")
        logging.error(f"Exception type: {type(e)}")
        import traceback
        logging.error("Full traceback:")
        logging.error(traceback.format_exc())
        return None

def generate_image(prompt, solution_id, generation_dir, assets_dir):
    """Generate an image using Replicate API and save it"""
    try:
        logging.info(f"Starting generation for {solution_id} with prompt: {prompt}")
        
        # Create workflow JSON with the prompt
        workflow_json = create_workflow_json(prompt)
        
        # Create prediction using replicate client
        try:
            logging.info("Starting Replicate API call...")
            model = "aleksa-codes/flux-ghibsky-illustration:a9f94946fa0377091ac0bcfe61b0d62ad9a85224e4b421b677d4747914b908c0"
            input_params = {
                "prompt": prompt + ", Ghibli art style, ancient Greek theme, highly detailed",
                "width": 768,
                "height": 1024,
                "num_outputs": 1
            }
            logging.info(f"Model: {model}")
            logging.info(f"Input parameters: {json.dumps(input_params, indent=2)}")
            
            # Create prediction using run method
            output = replicate.run(
                model,
                input=input_params
            )
            logging.info("Replicate API call completed successfully")
        except Exception as e:
            logging.error(f"Error during Replicate API call: {str(e)}")
            logging.error(f"Exception type: {type(e)}")
            import traceback
            logging.error("Full traceback:")
            logging.error(traceback.format_exc())
            return None, None
        
        logging.info(f"Model output: {output}")
        
        # Get the image URL from the output
        logging.info(f"Raw output from Replicate: {output}")
        
        if output is None:
            logging.error("Received None output from Replicate API")
            return None, None
            
        # Handle different possible output formats
        if isinstance(output, list) and len(output) > 0:
            image_url = str(output[0])  # Ensure we have a string URL
        elif isinstance(output, dict) and 'output' in output:
            image_url = str(output['output'])
        elif isinstance(output, str):
            image_url = output
        else:
            logging.error(f"Unexpected output format from Replicate API: {type(output)}")
            return None, None
            
        if not image_url:
            logging.error("No valid image URL found in the output")
            return None, None
            
        logging.info(f"Got image URL: {image_url}")
        
        # Download the image
        local_path = download_image(image_url, solution_id, assets_dir, generation_dir)
        
        if local_path:
            # Save metadata
            metadata = {
                "prompt": prompt,
                "url": image_url,
                "local_path": local_path,
                "generated_at": datetime.now().isoformat(),
                "solution_id": solution_id
            }
            
            metadata_path = os.path.join(generation_dir, f"{solution_id}_metadata.json")
            with open(metadata_path, "w", encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return image_url, local_path
        else:
            logging.error("Failed to download image")
            return None, None
            
    except Exception as e:
        logging.error(f"Error generating image for {solution_id}: {str(e)}")
        logging.error(f"Exception type: {type(e)}")
        import traceback
        logging.error("Full traceback:")
        logging.error(traceback.format_exc())
        return None, None

def main():
    """Main function to generate images for all solutions"""
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
        # Create directories
        generation_dir, assets_dir = create_directories()
        logging.info(f"Created directories: Generation={generation_dir}, Assets={assets_dir}")
        
        # Initialize summary data
        summary_data = {}
        
        # Process all solutions
        for solution_id, solution_data in SOLUTIONS.items():
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
            total_solutions = len(SOLUTIONS)
            current_solution = list(SOLUTIONS.keys()).index(solution_id) + 1
            logging.info(f"Progress: {current_solution}/{total_solutions} solutions processed")
            if current_solution < total_solutions:
                delay = 5
                logging.info(f"Waiting {delay} seconds before next generation...")
                time.sleep(delay)
        
        # Save summary
        summary_path = os.path.join(generation_dir, "summary.json")
        with open(summary_path, "w", encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        # Log final statistics
        successful = len([s for s in summary_data.values() if s.get('local_path')])
        total = len(SOLUTIONS)
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
