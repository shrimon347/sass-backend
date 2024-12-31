from g4f.client import Client

client = Client()

# Define parameters
model = "flux"  # Ensure this is the correct model name
prompt = "a white siamese cat"

quality = "standard"  # Specify the quality of the image
n = 2  # Number of images to generate

try:
    # Generate images using the specified model
    response = client.images.generate(
        model=model,
        prompt=prompt,
      
        quality=quality,
        n=n  # Generate n images
    )

    # Extract URLs of the generated images
    image_urls = [image.url for image in response.data]

    # Print all generated image URLs
    for index, image_url in enumerate(image_urls):
        print(f"Generated image {index + 1} URL: {image_url}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
