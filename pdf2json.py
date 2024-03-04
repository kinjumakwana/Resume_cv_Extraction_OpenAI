import json
import time
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
# from langchain.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain.schema import HumanMessage, SystemMessage
import jsbeautifier
from function_template import *
import logging
import os
from dotenv import load_dotenv
# from langchain.llms import HuggingFaceHub
from langchain_community.llms import HuggingFaceHub

# Load environment variables from .env file
# load_dotenv()

print("Call pf2df2json ")
model_name = "gpt-3.5-turbo-16k"
# Create logger for this module
logger = logging.getLogger(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir", basedir)
logger.info("basedir", basedir)

# import openai
# openai.api_key = "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"

# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "user", "content": "Tell the world about the ChatGPT API in the style of a pirate."}
#   ]
# )

# print(completion.choices[0].message.content)

CV_UPLOAD_DIR = "./cv_upload/"
CV_ANALYSIS_DIR = "./cv_analysis/"
GPT_MODEL = "gpt-3.5-turbo-0613"
# My 
OPENAI_API_KEY="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"

# Final
# OPENAI_API_KEY="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"
# OPENAI_API_KEY="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"

HF_MODEL = "HuggingFaceH4/zephyr-7b-beta"
HF_API_KEY = "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"
        

def output2json(output):
    """GPT Output Object >>> json"""
    logger.info("Call output2json")
    # output_string = ast.literal_eval(output.function_call.arguments)
    print("output: ",output)
    opts = jsbeautifier.default_options()
    return json.loads(jsbeautifier.beautify(output["function_call"]["arguments"], opts))

def json2file(data, file_dir, file_name):
    """write json to file"""
    logger.info("Call json2file")
    with open(file_dir + file_name, "w") as outfile:
        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        outfile.write(jsbeautifier.beautify(json.dumps(data), opts))

class DocumentAnalyzer:
    def __init__(self):
        self.cv_upload_dir = CV_UPLOAD_DIR
        self.cv_analysis_dir = CV_ANALYSIS_DIR
        self.fn_cv_analysis = fn_cv_analysis
        self.system_prompt_candidate = system_prompt_candidate
        self.system_prompt_jd = system_prompt_jd
        self.openai_api_key = OPENAI_API_KEY
        print(self.openai_api_key)
        # self.hf_api_key = HF_API_KEY

        # Get OpenAI API key from environment variable
        # self.openai_api_key = os.getenv("OPENAI_API_KEY")
        # if not self.openai_api_key:
        #     raise ValueError("OpenAI API key is not set in the environment variable OPENAI_API_KEY.")
        # print("Call class DocumentAnalyzer")

    def load_pdf_docx(self, file_path):
        logger.info("call load_pdf_docx")
        file_path = os.path.abspath(file_path)  # Get absolute path
        logger.info("File path:", file_path)
        if os.path.basename(file_path).endswith(".pdf") or os.path.basename(
            file_path
        ).endswith(".PDF"):
            loader = PyPDFLoader(file_path)
        elif os.path.basename(file_path).endswith(".docx") or os.path.basename(
            file_path
        ).endswith(".DOCX"):
            loader = Docx2txtLoader(file_path)

        documents = loader.load_and_split()
        return documents
    
    def json_filename(self, file_name):
        """abc.pdf >>> abc.json"""
        logger.info("Call json_filename.")
        base_name, file_extension = os.path.splitext(file_name)
        json_filename = base_name + ".json"
        return json_filename
    
    def get_cv(self, uploaded_file):
        """load 1 CV to string"""
        logger.info("call get_cv.....")
        
        # Extracting the file name from the UploadedFile object
        file_name = uploaded_file.name
        file_path = os.path.join(self.cv_upload_dir, file_name)

        # Create directory if it doesn't exist
        os.makedirs(self.cv_upload_dir, exist_ok=True)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        data = self.load_pdf_docx(file_path=file_path)
        _context = ""
        for x in data:
            _context = _context + x.page_content

        logger.info("Data:", data)
        logger.info("_context:", _context)
        return _context
    
    def analyse_candidate(self, file_name):
        start = time.time()
        logger.info("Start analyse candidate/ call analyse_candidate")

        content = self.get_cv(file_name)
        logger.info(f"Time read CV: {time.time() - start}")

        print(content)
        # return content

        llm = ChatOpenAI(api_key=self.openai_api_key,model=model_name, temperature=0.5)
        # llm = HuggingFaceHub(huggingfacehub_api_token=self.hf_api_key ,repo_id=HF_MODEL, model_kwargs={"temperature":0.5, "max_length":512})

        completion = llm.predict_messages(
            [
                SystemMessage(content=system_prompt_candidate),
                HumanMessage(content=content),
            ],
            functions=fn_cv_analysis,
        )

        output_analysis = completion.additional_kwargs
        print("output_analysis: ", output_analysis)

        json_output = output2json(output=output_analysis)
        print("json_output: ", json_output)
        
        # Construct file name based on candidate's name
        candidate_name = json_output["PersonalInformation"]["name"]
        file_name_json = f"{candidate_name}.json"

        # Define file path for the JSON file in the cv_analysis directory
        file_path_json = os.path.join(self.cv_analysis_dir, file_name_json)
        
        # Create directory if it doesn't exist
        os.makedirs(self.cv_analysis_dir, exist_ok=True)

        # Save json_output as a JSON file
        with open(file_path_json, "w") as json_file:
            json.dump(json_output, json_file, indent=4)

        # file_name_json = self.json_filename(file_name=file_name)
        # json2file(
        #     data=json_output, file_dir=self.cv_analysis_dir, file_name=file_name_json
        # )

        logger.info("Done analyse candidate")
        logger.info(f"Time analyse candidate: {time.time() - start}")

        recommended_jobs = recommended_jobs = ", ".join(json_output["JobRecommend"])
        return {
            "name": json_output["PersonalInformation"]["name"],
            "phone": json_output["PersonalInformation"]["phone"],
            "email": json_output["PersonalInformation"]["email"],
            "summary": json_output["Comment"],
            "recommended_jobs": recommended_jobs,
        }

