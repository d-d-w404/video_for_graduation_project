# Video Annotation Tool

A PyQt5-based video annotation tool designed for bounding box labeling in video frames. This tool is particularly useful for computer vision projects, especially for preparing training data for object detection and tracking tasks.

## Code Structure

### Main Components

```
video_for_graduation_project/
├── draw_bounding_box/
│   ├── video/
│   │   ├── video.py              # Main application file
│   │   ├── find_bounding_box.py  # Bounding box detection utilities
│   │   ├── image_processing.py   # Image processing functions
│   │   └── other utility files...
│   ├── Binary_search_frame/      # Binary search implementation
│   ├── store/                    # Stored annotation images
│   ├── target_pic/              # Target images for annotation
│   └── temp_pic/                # Temporary image storage
└── requirements.txt             # Python dependencies
```

### Core Classes

#### 1. `Video` Class (Main Application)
- **Purpose**: Main application window and video player
- **Key Features**:
  - Video loading and playback control
  - Binary search frame navigation
  - File management interface
  - Data export functionality

#### 2. `myLabel` Class (Custom Label Widget)
- **Purpose**: Custom QLabel for interactive bounding box drawing
- **Key Features**:
  - Mouse event handling for drawing rectangles
  - Real-time bounding box adjustment
  - Support for multiple annotation types (human/ball)
  - Drag and resize functionality

### Key Global Variables

```python
# Annotation data storage
pos_human = [0,0,0,0]  # Human bounding box coordinates
pos_ball = [0,0,0,0]   # Ball bounding box coordinates

# Text output format
text_0 = ""  # Frame range information
text_1 = ""  # Left frame annotation
text_2 = ""  # Middle frame annotation  
text_3 = ""  # Right frame annotation

# File paths
source_file_name = ""  # Source video directory
target_file_path = ""  # Output annotation directory
```

## Installation

### Prerequisites
- Python 3.6+
- PyQt5
- OpenCV

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd video_for_graduation_project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python draw_bounding_box/video/video.py
```

## How to Use

### 1. Initial Setup

#### Setting File Paths
- **SOURCE_PATH**: Click the "SOURCE_PATH" button to set the directory containing your video files
- **FILE_PATH**: Click the "FILE_PATH" button to set the output directory for annotation data

#### Loading Videos
- **Method 1**: Click "Load" button and select a video file
- **Method 2**: Double-click on a video file in the file tree (right panel)

### 2. Video Navigation

#### Basic Controls
- **Load**: Load a new video file
- **Stop**: Stop current video and clear annotations
- **Pause**: Pause/resume video playback
- **Progress Bar**: Drag to navigate through video frames

#### Binary Search Navigation
- **Left Arrow (←)**: Move right boundary to middle, focus on left half
- **Right Arrow (→)**: Move left boundary to middle, focus on right half
- **R Key**: Undo last binary search step
- **A Key**: Jump to left boundary
- **D Key**: Jump to right boundary
- **S Key**: Jump to middle position

#### Fine Adjustment
- **W Key**: Lock/unlock boundary labels for precise adjustment
- **Q Key**: Move one frame backward
- **E Key**: Move one frame forward

### 3. Annotation Process

#### Drawing Bounding Boxes
1. **Select Annotation Type**:
   - Press **1**: Switch to human annotation mode (green boxes)
   - Press **2**: Switch to ball annotation mode (red boxes)

2. **Draw Bounding Box**:
   - Click and drag mouse to draw a rectangle
   - Double-click to clear current annotation
   - Drag box edges to resize
   - Drag box center to move

3. **Save Annotation**:
   - Press **Space**: Save current frame annotation
   - Press **M**: Export all annotations to file

### 4. Data Export

#### Annotation Format
The tool exports data in the following format:
```
frame_range_left,frame_range_right
human_x0,human_y0,human_x1,human_y1
human_x0,human_y0,human_x1,human_y1
human_x0,human_y0,human_x1,human_y1
```

Where:
- `frame_range_left,frame_range_right`: The frame range being annotated
- `human_x0,human_y0,human_x1,human_y1`: Bounding box coordinates (top-left and bottom-right corners)

#### Export Process
1. Annotate frames at left boundary, middle, and right boundary
2. Press **M** to save annotations
3. Data is saved as `.txt` files in the specified output directory
4. File naming: `video_name.txt` (special characters replaced with safe alternatives)

### 5. Keyboard Shortcuts Summary

| Key | Function |
|-----|----------|
| **1** | Switch to human annotation mode |
| **2** | Switch to ball annotation mode |
| **Space** | Save current frame annotation |
| **M** | Export annotations to file |
| **←** | Binary search: focus left half |
| **→** | Binary search: focus right half |
| **R** | Undo binary search step |
| **A** | Jump to left boundary |
| **D** | Jump to right boundary |
| **S** | Jump to middle position |
| **W** | Lock/unlock boundary adjustment |
| **Q** | Move one frame backward |
| **E** | Move one frame forward |
| **P** | Pause/resume video |
| **Shift** | Close success dialog |

## Technical Details

### Binary Search Algorithm
The tool implements a binary search algorithm for efficient frame navigation:
- Maintains left and right boundaries
- Calculates middle position for navigation
- Stores search history for undo functionality
- Visual indicators show current search range

### Annotation Data Structure
- **Human annotations**: Green bounding boxes for person detection
- **Ball annotations**: Red bounding boxes for ball/object detection
- **Frame range**: Specifies the temporal extent of annotations
- **Coordinate system**: Top-left origin with pixel coordinates

### File Management
- **Source directory**: Contains input video files
- **Output directory**: Stores annotation data files
- **Temporary storage**: Manages intermediate processing files
- **File validation**: Checks for existing files and data completeness

##  Troubleshooting

### Common Issues
1. **Video not loading**: Ensure video format is supported (.mp4, .avi)
2. **Annotations not saving**: Check if output directory is properly set
3. **Interface not responding**: Verify PyQt5 installation
4. **File path errors**: Use forward slashes in file paths

### Performance Tips
- Use shorter video clips for better responsiveness
- Close other applications to free up memory
- Ensure sufficient disk space for output files

## Notes

- The tool automatically pauses video when first loaded
- Binary search is most effective for long videos
- Annotations are validated before export
- The interface supports both mouse and keyboard interaction
- All annotations are saved in pixel coordinates

##  Contributing

Feel free to submit issues and enhancement requests. This tool is designed for academic and research purposes, particularly for computer vision projects requiring video annotation.

##  License

This project is intended for educational and research purposes. Please ensure compliance with any applicable licenses for the libraries used.
