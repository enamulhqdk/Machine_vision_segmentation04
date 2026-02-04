import cv2
import matplotlib.pyplot as plt

#IMAGE_PATH = "images/robodk_imgN.png"   
#IMAGE_PATH = "images/real_1.png"      
#IMAGE_PATH = "images/real_2.png"
#IMAGE_PATH = "images/real_3.png"
IMAGE_PATH = "images/real_4.png"

img = cv2.imread(IMAGE_PATH)


if img is None:
    raise IOError("Image not found. Check the path or filename.")

# Convert to RGB and grayscale
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Otsu thresholding (objects = white)
_, img_bin = cv2.threshold(
    img_gray,
    0,
    255,
    cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)
# Morphological operations to clean noise
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)
img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernel)

# Connected components
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
    img_bin,
    connectivity=4,
    ltype=cv2.CV_32S
)

print(f"Detected objects (excluding background): {num_labels - 1}")

# Copy image for annotation
annotated = img_rgb.copy()

MIN_AREA = 800  # area threshold to remove small blobs

for i in range(1, num_labels):
    x, y, w, h, area = stats[i]

    if area < MIN_AREA:
        continue  # skip small noise blobs

    cx, cy = centroids[i]

    # Draw bounding box
    cv2.rectangle(
        annotated,
        (x, y),
        (x + w, y + h),
        (255, 0, 255),   # magenta
        2
    )
    
    # Draw centroid
    cv2.circle(
        annotated,
        (int(cx), int(cy)),
        4,
        (255, 0, 0),     # red
        -1
    )
    
    # Put centroid text
    cv2.putText(
        annotated,
        f"({int(cx)},{int(cy)})",
        (x, y - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (0, 255, 0),     # green
        1
    )

# Show annotated image
plt.figure(figsize=(6, 6))
plt.imshow(annotated)
plt.title("Detected Objects with Bounding Boxes and Centroids")
plt.axis("off")
plt.show()
cv2.imwrite("images/partA_binary.png", img_bin)
cv2.imwrite("images/partA_annotated.png", cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
