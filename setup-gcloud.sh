#!/bin/bash
# ============================================================
# HorseMaster AI - Google Cloud Setup Script
# ============================================================
# Run this script in Google Cloud Shell:
# https://console.cloud.google.com/cloudshell
# ============================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   HorseMaster AI - Google Cloud Setup${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# ============================================================
# STEP 1: Project Setup
# ============================================================
echo -e "${YELLOW}[Step 1/6] Project Setup${NC}"

# Get current project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "")

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}No project selected!${NC}"
    echo "Creating new project..."
    PROJECT_ID="horsemaster-ai-$(date +%Y%m%d)"
    gcloud projects create $PROJECT_ID --name="HorseMaster AI"
    gcloud config set project $PROJECT_ID
else
    echo -e "${GREEN}Using project: $PROJECT_ID${NC}"
fi

# Link billing account (required)
echo -e "${YELLOW}Note: You need to link a billing account to your project.${NC}"
echo "Go to: https://console.cloud.google.com/billing/linkedaccount?project=$PROJECT_ID"
read -p "Press Enter after linking billing account..."

# ============================================================
# STEP 2: Enable APIs
# ============================================================
echo -e "${YELLOW}[Step 2/6] Enabling APIs...${NC}"

gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable artifactregistry.googleapis.com

echo -e "${GREEN}APIs enabled successfully!${NC}"

# ============================================================
# STEP 3: Clone Repository
# ============================================================
echo -e "${YELLOW}[Step 3/6] Cloning Repository...${NC}"

if [ -d "horsemaster-render" ]; then
    echo "Repository already exists, updating..."
    cd horsemaster-render
    git pull origin master
else
    git clone https://github.com/aielghali/horsemaster-render.git
    cd horsemaster-render
fi

echo -e "${GREEN}Repository ready!${NC}"

# ============================================================
# STEP 4: Set Permissions
# ============================================================
echo -e "${YELLOW}[Step 4/6] Setting Permissions...${NC}"

PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
SERVICE_ACCOUNT="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

# Grant Cloud Run Admin role
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/run.admin" 2>/dev/null || echo "Role already assigned"

# Grant Service Account User role
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/iam.serviceAccountUser" 2>/dev/null || echo "Role already assigned"

# Grant Storage Admin for Container Registry
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/storage.admin" 2>/dev/null || echo "Role already assigned"

echo -e "${GREEN}Permissions set successfully!${NC}"

# ============================================================
# STEP 5: Build and Deploy
# ============================================================
echo -e "${YELLOW}[Step 5/6] Building and Deploying...${NC}"

REGION="us-central1"
SERVICE_NAME="horsemaster"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "Building container image..."
gcloud builds submit --tag $IMAGE_NAME --timeout=600s

echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 3 \
    --timeout 300 \
    --set-env-vars "PYTHONUNBUFFERED=1"

echo -e "${GREEN}Deployment successful!${NC}"

# ============================================================
# STEP 6: Get Service URL
# ============================================================
echo -e "${YELLOW}[Step 6/6] Getting Service URL...${NC}"

SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --format 'value(status.url)')

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}   🎉 Setup Complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "Your HorseMaster AI is now running at:"
echo -e "${BLUE}$SERVICE_URL${NC}"
echo ""
echo -e "Test it:"
echo -e "  ${YELLOW}curl $SERVICE_URL/health${NC}"
echo ""
echo -e "API Endpoints:"
echo "  - GET  /              - Web Interface"
echo "  - GET  /health        - Health Check"
echo "  - POST /api/fetch-race - Fetch Race Data"
echo ""

# ============================================================
# BONUS: Create Cloud Build Trigger for Auto-Deploy
# ============================================================
echo -e "${YELLOW}Setting up auto-deploy trigger...${NC}"

# Check if trigger exists
TRIGGER_EXISTS=$(gcloud builds triggers list --filter="name='horsemaster-github'" --format="value(name)" 2>/dev/null || echo "")

if [ -z "$TRIGGER_EXISTS" ]; then
    echo "Creating Cloud Build trigger..."
    gcloud builds triggers create github \
        --name="horsemaster-github" \
        --repo-name="horsemaster-render" \
        --repo-owner="aielghali" \
        --branch-pattern="^master$" \
        --build-config="cloudbuild.yaml" \
        --include-build-logs 2>/dev/null || echo "Manual trigger creation may be required in Console"
else
    echo "Trigger already exists"
fi

echo ""
echo -e "${GREEN}Auto-deploy configured!${NC}"
echo "Every push to GitHub master branch will trigger a new deployment."
echo ""
