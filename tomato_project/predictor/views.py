from django.shortcuts import render, redirect 
from django.core.files.storage import FileSystemStorage 
from django.conf import settings 
import os 
import tensorflow as tf 
import numpy as np 
# --- Disease Information Dictionary (Includes all 10 classes) --- 
DISEASE_INFO = { 
    'Tomato_Bacterial_spot': { 
        'cause': "Caused by the bacteria Xanthomonas campestris pv. vesicatoria. It thrives in warm, wet conditions, spreading via infected seeds and wind-blown rain. Symptoms include dark, water-soaked spots on leaves and small scabs on fruit.", 
        'solution': "Use certified disease-free seeds and transplants. Apply copper-based bactericides early in the season. Ensure good air circulation and avoid overhead watering to minimize leaf wetness."    }, 
    'Tomato_Early_blight': { 
        'cause': "Caused by the fungus Alternaria solani. It affects leaves, stems, and fruit, particularly prevalent when temperatures are warm and moisture is high. Characterized by dark, concentric rings (bullseye) on older leaves.", 
        'solution': "Rotate crops annually (do not plant tomatoes/potatoes in the same spot for 23 years). Remove and destroy infected plant debris immediately. Apply preventative fungicides (e.g., chlorothalonil) weekly after the first signs."    }, 
    'Tomato_Late_blight': { 
        'cause': "Caused by the water mold Phytophthora infestans. Highly destructive and rapidly spreading in cool, wet weather. Symptoms are large, dark brown to black spots on leaves and fuzzy white mold on the undersides.", 

        'solution': "Destroy all infected plants immediately. Apply highly effective fungicides (mancozeb or chlorothalonil) preventatively when cool, wet weather is forecast. Ensure maximum air circulation."    }, 
    'Tomato_Leaf_Mold': { 
        'cause': "Caused by the fungus Passalora fulva (Cladosporium fulvum). It's primarily a greenhouse disease but can occur outdoors in high humidity. Symptoms include velvety, olive-green to brown patches on the lower leaf surface.", 
        'solution': "Improve air circulation by pruning and spacing plants. Lower humidity in greenhouses. Apply fungicides specifically registered for leaf mold (e.g., maneb, chlorothalonil) if necessary."    }, 
    'Tomato_Septoria_leaf_spot': { 
        'cause': "Caused by the fungus Septoria lycopersici. Spreads by splashing water and rain. Characterized by small, circular spots with dark borders and gray/white centers on the leaves, usually starting at the bottom.", 
        'solution': "Water plants at the base, avoiding wetting the foliage. Remove and destroy infected leaves promptly. Apply fungicides such as chlorothalonil or copper products upon disease detection."    }, 
    'Tomato_Spider_mites_Two-spotted_spider_mite': { 
        'cause': "Caused by the two-spotted spider mite (Tetranychus urticae). These tiny pests feed on the underside of leaves, causing fine stippling (tiny yellow dots) and, in heavy infestations, webbing.", 
        'solution': "Use a strong jet of water to dislodge mites. Apply insecticidal soaps or horticultural oils directly to the mites, focusing on the undersides of leaves. Introduce beneficial predatory mites if feasible."    }, 
    'Tomato_Target_Spot': { 
        'cause': "Caused by the fungus Corynespora cassiicola. Favors warm temperatures and high humidity. Produces distinctive target-like spots (concentric rings) on the leaves, similar to Early Blight but often darker.", 
        'solution': "Practice crop rotation. Ensure good sanitation by removing plant debris. Apply registered fungicides (azoxystrobin or copper) early when conditions favor the disease."    }, 
    'Tomato_Tomato_Yellow_Leaf_Curl_Virus': { 
        'cause': "Caused by the Tomato Yellow Leaf Curl Virus (TYLCV) and transmitted exclusively by the Silverleaf whitefly (Bemisia tabaci). Infected leaves become small, curl upward, and turn pale yellow.", 
        'solution': "Control the whitefly vector using sticky traps and appropriate insecticides. Use resistant or tolerant tomato varieties. Remove and destroy infected plants immediately to prevent spread."    }, 
    'Tomato_Tomato_mosaic_virus': { 
        'cause': "Caused by the Tomato Mosaic Virus (ToMV) or Tobacco Mosaic Virus (TMV). Extremely contagious and spreads easily by touch, tools, or hands. Symptoms include a light and dark green mosaic pattern on leaves.", 
        'solution': "Use resistant varieties. Practice strict sanitation: wash hands and sterilize tools with a bleach solution (1:4 ratio) regularly. Immediately rogue (remove and destroy) infected plants." 
    }, 
    'Tomato_Healthy': { 
        'cause': 'N/A: The plant appears healthy.', 
        'solution': 'Continue monitoring your plant and maintain optimal care: consistent watering, balanced fertilization, and good air circulation.' 
    }} 
MODEL = None 
def load_model(): 
    global MODEL 
    if MODEL is None: 
        try: 
            # Adjust this path to where your model is saved 
            model_path = os.path.join(settings.BASE_DIR, 'predictor', 'model', 
'crop_disease_model.h5') 
            MODEL = tf.keras.models.load_model(model_path) 
            print("Model loaded successfully.") 
        except Exception as e: 
            print(f"Error loading model: {e}") 
            MODEL = None 
    return MODEL 
# Call load_model once when the server starts 
load_model() 
# --- END PLACEHOLDER --- 
# Function to preprocess the image for your specific model 
def preprocess_image(image_path): 
    # This is a generic example. Adjust to your model's required input (e.g., size, normalization) 
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(128, 128)) # Example size 
    img_array = tf.keras.preprocessing.image.img_to_array(img) 
    img_array = tf.expand_dims(img_array, 0)  # Create a batch dimension 
    # Add normalization/scaling as per your model (e.g., / 255.0) 
    return img_array 
def home_view(request): 
    """Simple view for the initial upload page (index.html).""" 
    return render(request, 'home.html') 
def about_view(request): 
    """Simple view for the about page (about.html).""" 
    return render(request, 'about.html') 
def contact_view(request): 
    """Simple view for the contact page (contact.html).""" 
    return render(request, 'contact.html') 
def predict_disease(request): 
    if request.method == 'POST' and 'tomato_leaf' in request.FILES: 
        uploaded_file = request.FILES['tomato_leaf'] 
        # 1. Save the image 
        fs = FileSystemStorage() 
        filename = fs.save(uploaded_file.name, uploaded_file) 
        uploaded_file_url = fs.url(filename) 
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, filename) 
 
        # 2. Get the model 
        model = load_model() 
        predicted_class_name = "Prediction failed. Model not loaded." 
        confidence = 0.0 
        predicted_class_id = 0 # Initialize to avoid errors 
        if model: 
            try: 
                # 3. Preprocess and Predict 
                input_tensor = preprocess_image(uploaded_file_path) 
                predictions = model.predict(input_tensor)[0]               
                # 4. Process results 
                class_names = [ 
                    'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight', 
                    'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two-spotted_spider_mite', 
                    'Tomato_Target_Spot', 'Tomato_Tomato_Yellow_Leaf_Curl_Virus', 'Tomato_Tomato_mosaic_virus', 
                    'Tomato_Healthy'                ] 
                predicted_class_id = np.argmax(predictions) 
                # FIX 1: Convert numpy.int64 to a standard Python integer (int) 
                # This solves the "TypeError: Object of type int64 is not JSON serializable" 
                predicted_class_id = int(predicted_class_id)  
                predicted_class_name = class_names[predicted_class_id] 
                confidence = float(predictions[predicted_class_id] * 100) 
            except Exception as e: 
                predicted_class_name = "Error during prediction: " + str(e) 
                predicted_class_id = 0 # Reset ID on error 
        # FIX 2: Correct the key name to 'disease_id' for consistency with show_result 
        request.session['last_prediction'] = { 
            'disease_name': predicted_class_name, 
            'confidence': f"{confidence:.2f}%", 
            'image_url': uploaded_file_url,        } 
        # Redirect to the result page 
        return redirect('show_result') 
    return redirect('home') 
# 3. Show Result View (New page after prediction) 
def show_result(request): 
    """Displays the prediction result and links to cause/solution.""" 
    # FIX 3: Correct variable name to match the session content 
    prediction_data = request.session.get('last_prediction', None) 
    if not prediction_data or'disease_name' not in prediction_data: 
        # If the user somehow landed here without predicting 
        return redirect('home') 
    # Get the ID (which is now a standard int) 
    disease_name = prediction_data.get('disease_name')  
    if not isinstance(disease_name,str): 
        return redirect('home') 
    disease_slug = disease_name.replace(' ', '_').replace('-', '_') 
    context = { 
        # 'disease' for display (spaces instead of underscores) 
        'disease': disease_name.replace('_', ' ').replace('-', ' '), 
        'confidence': prediction_data['confidence'], 
        'image_url': prediction_data['image_url'], 
        'disease_slug': disease_slug, # Used for URL generation in the template 
        'disease_info_available': disease_slug in DISEASE_INFO    } 
    return render(request, 'result.html', context) 
# 4. Show Cause View 
def show_cause(request, disease_name): 
    """Displays the cause for the specified disease.""" 
    # 'disease_name' here is the URL slug (e.g., Tomato_Bacterial_spot) 
    info = DISEASE_INFO.get(disease_name) 
    # Prepare the name for display in the template 
    clean_name = disease_name.replace('_', ' ') 
    context = { 
        'disease': clean_name, 
        'heading': f"Causes of {clean_name}", 
        'content': info['cause'] if info else "Cause information not available.",    } 
    return render(request, 'cause.html', context) 
# 5. Show Solution View 
def show_solution(request, disease_name): 
    """Displays the solution for the specified disease.""" 
    # 'disease_name' here is the URL slug (e.g., Tomato_Bacterial_spot) 
    info = DISEASE_INFO.get(disease_name) 
    # Prepare the name for display in the template 
    clean_name = disease_name.replace('_', ' ')     
    context = { 
        'disease': clean_name, 
        'heading': f"Preferred Solution for {clean_name}", 
        'content': info['solution'] if info else "Solution information not available.",    } 
    return render(request, 'solution.html', context) 
# 6. Progress Tracking View (Placeholder for future logic) 
def progress_view(request): 
    """Allows farmers to upload a new image and track progress.""" 
 
    return render(request, 'progress.html', {'message': 'Upload a new image to check progress.'})