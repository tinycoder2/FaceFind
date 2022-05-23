# from dataclasses import dataclass
# from os import listdir
# from os.path import isfile, join
# import io
# import json
# from azure.cognitiveservices.vision.face import FaceClient
# from msrest.authentication import CognitiveServicesCredentials
# import requests
# from PIL import Image, ImageDraw, ImageFont

# """
# Example 4. Detect if a face shows up in other photos/images
# """

# # face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# # database = [f for f in listdir(r'.\media\missingpersons') if isfile(join(r'.\media\missingpersons', f))]

# # print(database)

# # face_ids=[]
# # # detected_faces=[]
# # for missing_person in database:
# #     response_detected_face = face_client.face.detect_with_stream(
# #         image=open(join(r'.\database', missing_person), 'rb'),
# #         detection_model='detection_03',
# #         recognition_model='recognition_04',  
# #     )
# #     face_ids.append(response_detected_face[0].face_id)
# #     # detected_faces.append(face for face in response_detected_face)

# # print(face_ids)

# # db=dict(zip(database, face_ids))

# # img_source = open(r'.\imgs\jeffbezos2.jpg', 'rb')
# # response_face_source = face_client.face.detect_with_stream(
# #     image=img_source,
# #     detection_model='detection_03',
# #     recognition_model='recognition_04'    
# # )
# # face_id_source = response_face_source[0].face_id
# # print(face_id_source)

# # matched_faces = face_client.face.find_similar(
# #     face_id=face_id_source,
# #     face_ids=face_ids
# # )

# # for matched_face in matched_faces:
# #     print("conf", matched_face.confidence)
# #     person = [k for k, v in db.items() if v == matched_face.face_id]
# #     print(person)


# ##
# # #load s3 credentials settings from configuration from a csv file
# #     with open(S3_KEY_DIR) as csv_file:
# #         csv_reader = csv.reader(csv_file, delimiter=',')

# #         # eliminate blank rows if they exist
# #         rows = [row for row in csv_reader if row]
# #         headings = rows[0] # get headings
# #         values = rows[1] # get values

# #     s3_keys = {}
# #     for heading, value in zip(headings, values):
# #         s3_keys[heading] = value 

# #     # AWS bucket settings
# #     AWS_ACCESS_KEY_ID = s3_keys['Access key ID']
# #     AWS_SECRET_ACCESS_KEY = s3_keys['Secret access key']
# #     AWS_STORAGE_BUCKET_NAME = s3_keys['User name']