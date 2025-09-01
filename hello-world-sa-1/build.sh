
IMAGE_NAME="hello-world-sa-1"

# detect architecture
ARCH=$(uname -m)
case "$ARCH" in
    x86_64)
        PLATFORM="linux/amd64"
        SUFFIX="amd"
        ;;
    aarch64 | arm64)
        PLATFORM="linux/arm64"
        SUFFIX="arm"
        ;;
    *)
        echo "❌ Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

TAG="${SUFFIX}"
REMOTE="zewang42/${IMAGE_NAME}:${TAG}"

echo "✅ Detected architecture: $ARCH"
echo "✅ Building for $PLATFORM"
echo "✅ Tagging as $REMOTE"

# build & push
docker buildx build \
    --platform "$PLATFORM" \
    -t "$REMOTE" \
    --push .

echo "🎉 Done: pushed $REMOTE"
