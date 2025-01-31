# Solution Image Generator

This script generates images for each OdissAI solution using Replicate's Stable Diffusion model.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file from the template:
```bash
cp .env.example .env
```

3. Add your Replicate API token to the `.env` file:
- Get your API token from https://replicate.com/account
- Replace `your_replicate_api_token_here` in `.env` with your actual token

## Usage

Run the script:
```bash
python generate_solution_images.py
```

The script will:
1. Create a dated folder in `generations/` to store all generated images and metadata
2. Generate an image for each solution using carefully crafted prompts
3. Save metadata for each generation including prompts and URLs
4. Create a summary.txt file with all generated image URLs

## Output Structure

```
generations/
└── YYYY-MM-DD_HH-MM-SS/
    ├── formation_metadata.json
    ├── agents_metadata.json
    ├── applications_metadata.json
    ├── conseil_metadata.json
    ├── hebergement_metadata.json
    ├── renforcement_metadata.json
    └── summary.txt

assets/
└── images/
    └── solutions/
        └── [generated images]
```

## Solutions

The script generates images for the following solutions:
- Formation des Équipes
- Agents IA sur Mesure
- Applications IA Rapides
- Conseil en Transformation IA
- Hébergement Sécurisé
- Renforcement des Équipes

Each solution has a carefully crafted prompt to generate relevant and professional images that match OdissAI's brand identity.
