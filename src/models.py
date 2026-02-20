from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class ResumeData:
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    experience: List[Dict] = field(default_factory=list)
    education: List[Dict] = field(default_factory=list)
    is_editing: bool = False
    pdf_generated: bool = False
    
    def is_complete(self) -> bool:
        return all([
            self.full_name,
            self.email,
            self.phone,
            self.skills,
            self.experience,
            self.education
        ])
    
    def get_missing_fields(self) -> List[str]:
        missing = []
        if not self.full_name: missing.append("full name")
        if not self.email: missing.append("email")
        if not self.phone: missing.append("phone number")
        if not self.skills: missing.append("skills")
        if not self.experience: missing.append("work experience")
        if not self.education: missing.append("education")
        return missing

class ConversationState:
    def __init__(self):
        self.sessions: Dict[str, ResumeData] = {}
    
    def get_or_create(self, user_id: str) -> ResumeData:
        if user_id not in self.sessions:
            self.sessions[user_id] = ResumeData()
        return self.sessions[user_id]
    
    def clear(self, user_id: str):
        if user_id in self.sessions:
            del self.sessions[user_id]
