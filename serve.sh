#!/bin/bash
# Simple web server for serving VR gallery scenes

PORT=${1:-8080}

echo "🌐 Starting VR Gallery Web Server"
echo "=================================="
echo ""
echo "📂 Serving from: $(pwd)"
echo "🔗 Port: $PORT"
echo ""
echo "🎨 Access your galleries:"
echo "   http://localhost:$PORT/sceneOutput/"
echo ""
echo "📊 API Server:"
echo "   http://localhost:8000/docs (if running)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="
echo ""

python -m http.server $PORT
