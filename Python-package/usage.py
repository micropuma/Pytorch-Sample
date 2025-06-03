from mlpredictor import MLPredictor

predictor = MLPredictor()
predictor.train()
prediction = predictor.predict([5.1, 3.5, 1.4, 0.2])
print("Predicted class:", prediction.item())

# Predicted class: 0
