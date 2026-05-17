# Smart Classroom Monitoring System (Face Recognition)

A Python-based **face recognition system** designed for smart classroom monitoring. It detects and recognizes registered students using a webcam.

---

## Features

* Face detection using `face_recognition` library
* Face encoding and training from custom dataset(used actor and actress images for datasets(easily available images))
* Real-time recognition via webcam
* Supports multiple known persons (students/teachers)

---

## Project Structure

```
project/
│
├── datasets/  (contains data images)
├── encodings/encodings.pkl (generated after training)
├── attendance/*.csv   (for each day attendance is stored in seperates csv files)
├── src/
│   ├── train.py
│   ├── recognize.py
│   └── attendance.py  
└── README.md    (this file)
```

---

## Installation

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Dataset Format

Each person should have a separate folder inside `datasets/`:

```
datasets/
├── 01_rajesh_hamal/
│   ├── 01_01.jpg
│   ├── 01_02.jpg
│   └── ...
├── 02_biraj_bhatta/
    ├── 02_01.jpg
    ├── 02_02.jpg
```
> it splits 01_rajesh_hamal to (01 and rajesh_hamal) for (rollno and name)

Use **clear face images** (10–20 images per person recommended).

---

## How to Train Model

Run:

```bash
python src/train.py
```

This will:

* Load images from `datasets/`
* Extract face encodings
* Save encodings to a file (e.g., `encodings.pkl`)

---

## Run Face Recognition

After training:

```bash
python src/recognize.py
```

It will:

* Open webcam
* Detect faces
* Match with trained dataset
* Display names on screen

---

### 3. dlib installation

```bash
sudo apt update
sudo apt install build-essential
```

---

## Future Improvements

* Add GUI dashboard
* Use deep learning model (FaceNet / ArcFace)

---

## Author

**Bishwa Ghimire**

BSc CSIT, Tribhuvan University
