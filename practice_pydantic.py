from pydantic import ValidationError
from app.schemas.document import DocumentUpload

def test_guards():
    # ==========================================
    # TEST 1: Bilkul Sahi Data
    # ==========================================
    print("--- TEST 1: Sahi Data ---")
    good_data = {"filename": "my_resume.pdf", "file_size_mb": 4.5}
    
    # 1. model_validate: Dictionary ko check karke Object banana
    safe_doc = DocumentUpload.model_validate(good_data)
    print("✅ Guard ne pass kar diya. Object ban gaya:", safe_doc.filename)
    
    # 2. model_dump: Object ko wapas Dictionary banana
    final_dict = safe_doc.model_dump()
    print("🔄 Wapas Dictionary me badla:", final_dict)

    # ==========================================
    # TEST 2: Galat Extension (Virus)
    # ==========================================
    print("\n--- TEST 2: Galat File Type ---")
    bad_type_data = {"filename": "hack.exe", "file_size_mb": 1.2}
    try:
        DocumentUpload.model_validate(bad_type_data)
    except ValidationError as error:
        print("❌ Guard ne rok liya! Error mila:")
        print(error.errors()[0]['msg']) # Sirf main error message print karega

    # ==========================================
    # TEST 3: TXT fail size limit (model_validator test)
    # ==========================================
    print("\n--- TEST 3: Badi TXT File ---")
    bad_txt_data = {"filename": "novel.txt", "file_size_mb": 5.0}
    try:
        DocumentUpload.model_validate(bad_txt_data)
    except ValidationError as error:
        print("❌ Guard ne rok liya! Error mila:")
        print(error.errors()[0]['msg'])

if __name__ == "__main__":
    test_guards()