from pydantic import BaseModel, field_validator, model_validator

# Ye Guard check karega jab user koi document upload karne ki koshish karega
class DocumentUpload(BaseModel):
    filename: str
    file_size_mb: float

    # 1. FIELD VALIDATOR: Sirf ek chiz check karta hai (File ka type)
    @field_validator("filename")
    @classmethod
    def validate_extension(cls, v: str) -> str:
        # Agar file in 3 types me se nahi hai, toh error phek do
        if not v.lower().endswith((".pdf", ".txt", ".docx")):
            raise ValueError("Sirf PDF, TXT, ya DOCX files allowed hain!")
        return v

    # 2. FIELD VALIDATOR: File size check karna (Max 10MB)
    @field_validator("file_size_mb")
    @classmethod
    def validate_size(cls, v: float) -> float:
        if v > 10.0:
            raise ValueError("File size 10MB se bada nahi hona chahiye!")
        return v
        
    # 3. MODEL VALIDATOR: Pure form ko ek sath check karta hai
    @model_validator(mode='after')
    def check_suspicious_files(self) -> 'DocumentUpload':
        # Dono fields ko ek sath compare karna: agar TXT hai toh limit sirf 2MB honi chahiye
        if self.filename.lower().endswith(".txt") and self.file_size_mb > 2.0:
            raise ValueError("TXT files ke liye max size 2MB hai!")
        return self