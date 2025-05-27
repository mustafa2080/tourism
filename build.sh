#!/bin/bash

# Build script for Railway deployment

set -e  # Exit on any error

echo "Starting build process..."

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm ci --only=production

# Build Tailwind CSS
echo "Building Tailwind CSS..."
npm run build

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build process completed successfully!"
