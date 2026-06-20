import difflib
import nltk
from nltk.chat.util import Chat, reflections
import tkinter as tk

# The Number of FAQ questions is your choice to decide .

pairs = [

    [r"hello|hey|hi|helo|hlo|hii",
     ["Hi there! How can I help you today?",
      "What can I do for you?"]],

    # Fees
    [r"bca fee|bca fee|fee for bca|bca fee structure",
     ["The total fee for BCA at MM University Mullana is approximately ₹2.1–2.7 lakh for the complete 3-year course."]],

    [r"mca fees|mca fee|fee for mca|mca fee structure",
     ["The total fee for MCA at MM University Mullana is approximately ₹1.97 lakh for the complete course."]],

    [r"btech cse fees|fee for btech cse|cse fees",
     ["The total fee for B.Tech CSE at MM University Mullana is approximately ₹6.7–10.2 lakh for the 4-year course."]],

    [r"data science fees|btech data science fees",
     ["The total fee for B.Tech Data Science is generally similar to other B.Tech CSE specializations."]],

    [r"mba it fees|mba fees|fee for mba",
     ["The total fee for MBA IT at MM University Mullana is approximately ₹3.2 lakh for the complete course."]],

    [r"hostel fees|hostel fee structure",
     ["Hostel fees vary depending on room type and facilities. Please contact the admission office for the latest details."]],

    [r"scholarship|scholarships|fee concession",
     ["MM University offers scholarships and fee concessions based on eligibility criteria."]],

    [r"payment options|emi|installments",
     ["Fee payment can typically be made semester-wise or annually."]],

    [r"refund policy|fee refund",
     ["Fee refund is subject to university rules and UGC guidelines."]],

    [r"total fees|courses fees|fee structure",
     ["Popular course fees: BCA ~₹2.1–2.7 lakh, MCA ~₹1.97 lakh, B.Tech CSE ~₹6.7–10.2 lakh, MBA ~₹3.2 lakh."]],

    # Courses
    [r"bca|bachelor of computer applications",
     ["BCA (Bachelor of Computer Applications) is a 3-year undergraduate course focusing on programming, databases, web development, networking, and software engineering."]],

    [r"mca|master of computer applications",
     ["MCA (Master of Computer Applications) is a 2-year postgraduate course covering advanced software development, AI, cloud computing, cybersecurity, and data science."]],

    [r"btech cse|b\.tech cse|computer science engineering|computer science and engineering",
     ["B.Tech CSE is a 4-year engineering program covering programming, algorithms, software development, operating systems, networking, and emerging technologies."]],

    [r"btech data science|data science|cse data science",
     ["B.Tech Data Science specializes in data analytics, machine learning, statistics, big data technologies, and AI applications."]],

    [r"mba it|mba information technology|information technology mba",
     ["MBA in Information Technology combines business management with IT concepts such as project management, business analytics, and digital transformation."]],

    # Other Information
    [r"placement|placements|job opportunities",
     ["MM University provides placement assistance, industry interactions, training programs, and recruitment drives for eligible students."]],

    [r"hostel|accommodation",
     ["On-campus hostel facilities are available for both boys and girls with modern amenities and security."]],

    [r"internship|training",
     ["Students are encouraged to participate in internships, industrial training, and real-world projects to enhance practical skills."]],

    [r"admission|apply|enrollment",
     ["Admissions are based on eligibility criteria specified for each course. Contact the admission office for the latest admission process."]],

    [r"certificate|degree",
     ["Students receive a recognized degree upon successful completion of their respective programs."]],

    [r"bye|goodbye",
     ["Goodbye! Have a great day!"]]
]

faq_phrases = {
    "hello": "Hi there! How can I help you today?",
    "bca fee": "The total fee for BCA at MM University Mullana is approximately ₹2.1–2.7 lakh for the complete 3-year course.",
    "mca fee": "The total fee for MCA at MM University Mullana is approximately ₹1.97 lakh for the complete course.",
    "btech cse fee": "The total fee for B.Tech CSE at MM University Mullana is approximately ₹6.7–10.2 lakh for the 4-year course.",
    "data science fee": "The total fee for B.Tech Data Science is generally similar to other B.Tech CSE specializations.",
    "mba fee": "The total fee for MBA IT at MM University Mullana is approximately ₹3.2 lakh for the complete course.",
    "hostel fee": "Hostel fees vary depending on room type and facilities. Please contact the admission office for the latest details.",
    "scholarship": "MM University offers scholarships and fee concessions based on eligibility criteria.",
    "payment options": "Fee payment can typically be made semester-wise or annually.",
    "refund policy": "Fee refund is subject to university rules and UGC guidelines.",
    "bca course": "BCA (Bachelor of Computer Applications) is a 3-year undergraduate course focusing on programming, databases, web development, networking, and software engineering.",
    "mca course": "MCA (Master of Computer Applications) is a 2-year postgraduate course covering advanced software development, AI, cloud computing, cybersecurity, and data science.",
    "btech cse": "B.Tech CSE is a 4-year engineering program covering programming, algorithms, software development, operating systems, networking, and emerging technologies.",
    "data science": "B.Tech Data Science specializes in data analytics, machine learning, statistics, big data technologies, and AI applications.",
    "mba it": "MBA in Information Technology combines business management with IT concepts such as project management, business analytics, and digital transformation.",
    "placement": "MM University provides placement assistance, industry interactions, training programs, and recruitment drives for eligible students.",
    "hostel": "On-campus hostel facilities are available for both boys and girls with modern amenities and security.",
    "internship": "Students are encouraged to participate in internships, industrial training, and real-world projects to enhance practical skills.",
    "admission": "Admissions are based on eligibility criteria specified for each course. Contact the admission office for the latest admission process.",
    "certificate": "Students receive a recognized degree upon successful completion of their respective programs."
}

def fuzzy_response(user_input):
    text = user_input.lower().strip()
    if not text:
        return None

    best_answer = None
    best_score = 0.0

    for phrase, answer in faq_phrases.items():
        ratio = difflib.SequenceMatcher(None, text, phrase).ratio()
        token_overlap = len(set(text.split()) & set(phrase.split())) / max(len(set(phrase.split())), 1)
        score = max(ratio, token_overlap)

        if score > best_score:
            best_score = score
            best_answer = answer

    return best_answer if best_score >= 0.5 else None

chatbot = Chat(pairs, reflections)

def chatbot_response():
    user_input = entry.get().strip()

    if user_input:
        response = chatbot.respond(user_input)
        if not response:
            response = fuzzy_response(user_input) or "I am not sure about that!"

        chat_log.insert(
            tk.END,
            f"You: {user_input}\nRoboTutor: {response}\n\n"
        )

        entry.delete(0, tk.END)

        if user_input in ["bye", "goodbye"]:
            root.after(2000, root.destroy)


root = tk.Tk()
root.title("RoboTutor Chatbot")


chat_frame = tk.Frame(root)
chat_frame.pack(padx=10, pady=10, fill="both", expand=True)


scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side="right", fill="y")


chat_log = tk.Text(
    chat_frame,
    width=80,
    height=25,
    wrap="word",
    yscrollcommand=scrollbar.set
)
chat_log.pack(side="left", fill="both", expand=True)


scrollbar.config(command=chat_log.yview)


entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=5)


send_button = tk.Button(root, text="Send", command=chatbot_response)
send_button.pack(pady=5)

root.mainloop()