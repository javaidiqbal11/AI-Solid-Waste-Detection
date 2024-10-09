import tensorflow as tf

# Load the SavedModel
converter = tf.lite.TFLiteConverter.from_saved_model('/media/abark/2fce48c5-6aff-4b5d-8579-0b1d2b28aefa/projects/Waste_Management_System/runs/detect/train4/weights/best.pt')  # Replace with your SavedModel directory

# Set optimization flag
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Set the representative dataset
converter.representative_dataset = representative_dataset_generator

# Specify supported operations
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

# Ensure input and output tensors are int8
converter.inference_input_type = tf.uint8  # or tf.int8
converter.inference_output_type = tf.uint8  # or tf.int8

# Convert the model
tflite_quant_model = converter.convert()

# Save the quantized model
with open('/media/abark/2fce48c5-6aff-4b5d-8579-0b1d2b28aefa/projects/Waste_Management_System/runs/detect/train5/best_int8.tflite', 'wb') as f:
    f.write(tflite_quant_model)
