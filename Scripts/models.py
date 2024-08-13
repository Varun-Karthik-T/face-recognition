from deepface import DeepFace

model = DeepFace.build_model("Dlib")
model.model.summary()