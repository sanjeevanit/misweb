import face_recognition
import numpy as np

# Function to load known face encodings from the database
def load_known_face_encodings(students):
    known_encodings = []
    known_ids = []
    for student in students:
        known_image = face_recognition.load_image_file(student.admin.profile_img.path)
        known_encoding = face_recognition.face_encodings(known_image)[0]
        known_encodings.append(known_encoding)
        # Ensure that student ID is converted to an integer if it's not already
        try:
            student_id = int(student.st_idNo)
        except ValueError:
            print(f"Invalid student ID for student: {student}")
            continue  # Skip this student and proceed to the next one
        known_ids.append(student_id)
    return known_encodings, known_ids


# Function to recognize the student's face
def recognize_student_face(known_encodings, unknown_encoding, tolerance=0.6):
    face_distances = face_recognition.face_distance(known_encodings, unknown_encoding)
    match_indices = [index for index, face_distance in enumerate(face_distances) if face_distance <= tolerance]
    if len(match_indices) > 0:
        return match_indices[0]  # Return the index of the first matched face
    return None  # Return None if no match is found



