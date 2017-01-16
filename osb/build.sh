# BUILD THE IMAGE (replace all environment variables)
NOCACHE=true
BUILD_START=$(date '+%s')
docker build --force-rm=$NOCACHE --no-cache=$NOCACHE -t oracle/osb:12.2.1.2 -f Dockerfile_osb . || {
  echo "There was an error building the image."
  exit 1
}

BUILD_END=$(date '+%s')
BUILD_ELAPSED=`expr $BUILD_END - $BUILD_START`
