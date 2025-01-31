# Image Generation Scripts

These scripts generate images for the OdissAI solutions using the Replicate API.

## Configuration System

The scripts use a configuration file (`solutions_config.json`) to control which solutions need to be regenerated. This allows for selective regeneration of specific solution images rather than regenerating all images every time.

### Configuration File Structure

```json
{
  "solutions_to_regenerate": ["formation", "agents"],  // Array of solution IDs to regenerate
  "last_generation": "2025-01-31T18:00:00Z",          // Timestamp of last generation
  "generation_history": [                              // History of generations
    {
      "timestamp": "2025-01-31T18:00:00Z",
      "directory": "scripts/generations/2025-01-31_18-00-00"
    }
  ]
}
```

## Available Scripts

### 1. generate_solution_images.py
The original script that generates images for all solutions. Use this when you want to regenerate all images.

```bash
python scripts/generate_solution_images.py
```

### 2. generate_selected_images.py
A new script that only generates images for solutions specified in the configuration file. Use this when you want to regenerate specific images.

1. Edit `solutions_config.json` to specify which solutions need regeneration:
   ```json
   {
     "solutions_to_regenerate": ["formation", "conseil"],
     "last_generation": null,
     "generation_history": []
   }
   ```

2. Run the script:
   ```bash
   python scripts/generate_selected_images.py
   ```

The script will:
- Only regenerate images for solutions listed in `solutions_to_regenerate`
- Update the generation history
- Clear the `solutions_to_regenerate` list after completion

## Available Solution IDs

- `formation` - Formation des Équipes
- `agents` - Agents IA sur Mesure
- `applications` - Applications IA Rapides
- `conseil` - Conseil en Transformation IA
- `hebergement` - Hébergement Sécurisé
- `renforcement` - Renforcement des Équipes

## Example Usage

1. To regenerate all images:
   ```bash
   python scripts/generate_solution_images.py
   ```

2. To regenerate specific images:
   ```bash
   # First, edit solutions_config.json
   {
     "solutions_to_regenerate": ["formation", "conseil"],
     "last_generation": null,
     "generation_history": []
   }
   
   # Then run the selective generation script
   python scripts/generate_selected_images.py
   ```

## Generated Files

Both scripts will:
1. Create a timestamped directory in `scripts/generations/`
2. Save generated images in both:
   - `scripts/generations/[timestamp]/[solution].webp`
   - `scripts/assets/images/solutions/[solution].webp`
3. Save metadata for each generation in `scripts/generations/[timestamp]/[solution]_metadata.json`
4. Save a summary of the generation in `scripts/generations/[timestamp]/summary.json`
5. Save logs in `scripts/generations/generation.log`

## Directory Structure

```
scripts/
├── assets/
│   └── images/
│       └── solutions/          # Latest version of each solution image
├── generations/               # Historical generations with timestamps
│   ├── generation.log        # Generation logs
│   └── YYYY-MM-DD_HH-MM-SS/  # Timestamped directories for each generation
└── solutions_config.json     # Configuration file for selective generation
