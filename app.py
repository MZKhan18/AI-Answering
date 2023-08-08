import streamlit as st
import PyPDF2
from fpdf import FPDF
import openai
from bardapi import Bard
import os


st.title("Ai-Answering")

st.caption("This is a website where you can upload questions on any topic in pdf format and it will generate answers by using Google's Bard Ai or Open Ai's gpt. It can only genrate answers to atmost 20 questions from one pdf.")
types_index = ['Q) Q) {recommended}','1. 2.','1) 2)','i) ii)', 'a. b.', 'a) b)', 'A. B.', 'A) B)']
pdf_file = st.file_uploader("Upload Pdf File *")
indexing = st.selectbox("Enter Indexing : Q) Q) indexing is recommended ",types_index)
key = st.text_input("Enter Api Key *",type="password",placeholder="Your API Key")
context = st.text_input("Enter Context or Instructions for AI *",placeholder="write program in java language")
ai = st.selectbox("Select AI for answering *",('BARD AI',"OPEN AI"))

if st.button("Write Answers"):

    if pdf_file and key and context and indexing and ai:

        # fetching pdf and extracting texts/questions
        st.caption("Step 1 : extracting questions from pdf")
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page_text_list = []
        # for pages in pdf_reader.pages:
        #     page_text_list.append(pages.extract_text())
        pdf_page = pdf_reader.pages[0]
        if indexing == types_index[1]:
            index = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.','11.', '12.', '13.', '14.', '15.', '16.', '17.', '18.', '19.', '20.']
        elif indexing == types_index[2]:
            index = ['1)', '2)', '3)', '4)', '5)', '6)', '7)', '8)', '9)', '10)', '11)', '12)', '13)', '14)', '15)',
                     '16)', '17)', '18)', '19)', '20)']
        elif indexing == types_index[3]:
            index = ['i)', 'ii)', 'iii)', 'iv)', 'v)', 'vi)', 'vii)', 'viii)', 'ix)', 'x)', 'xi)', 'xii)', 'xiii)', 'xiv)', 'xv)',
                     'xvi)', 'xvii)', 'xviii)', 'xix)', 'xx)']
        elif indexing == types_index[4]:
            index = ['a.', 'b.', 'c.', 'd.', 'e.', 'f.', 'g.', 'h.', 'i.', 'j.','k.', 'l.', 'm.', 'n.', 'o.',
                     'p.', 'q.', 'r.', 's.', 't.']
        elif indexing == types_index[5]:
            index = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)', 'g)', 'h)', 'i)', 'j)', 'k)', 'l)', 'm)', 'n)', 'o)',
                     'p)', 'q)', 'r)', 's)', 't)']
        elif indexing == types_index[6]:
            index = ['A.', 'B.', 'C.', 'D.', 'E.', 'F.', 'G.', 'H.', 'I.', 'J.','K.', 'L.', 'M.', 'N.', 'O.',
                     'P.', 'Q.', 'R.', 'S.', 'T.']
        elif indexing == types_index[7]:
            index = ['A)', 'B)', 'C)', 'D)', 'E)', 'F)', 'G)', 'H)', 'I)', 'J)', 'K)', 'L)', 'M)', 'N)', 'O)',
                     'P)', 'Q)', 'R)', 'S)', 'T)']
        else:
            index = 0

        questions = []
        for single_page in pdf_reader.pages:
            text = single_page.extract_text()
            if index !=0:
                for rep in index:
                    text = text.replace('{}'.format(rep), 'Q)')
            q_list = text.split('Q)')
            q_list = q_list[1:]
            questions.extend(q_list)

        cont_ques = []
        for q in questions:
            ques = context + q
            cont_ques.append(ques)


        #giving questions to open ai and genrating answers IT HAS RATE LIMITS, ONLY 3 RPM
        st.caption("Step 2 : generating answers")
        if ai == 'OPEN AI':
            answers = []
            openai.api_key = key
            for q in questions:
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=[
                        {"role": "system", "content":context},
                        {"role": "user", "content": q}
                    ]
                )
                answers.append(chat.choices[0].message.content)


        # giving questions to bard and collecting answers
        elif ai == 'BARD AI':
            os.environ["_BARD_API_KEY"] = key
            answers = []
            for q in cont_ques:
                answers.append(Bard().get_answer(str(q))['content'])

        #writing answers in new pdf
        st.caption("Step 3 : creating new pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 20)
        pdf.cell(200, 10, txt="Answers By AI", ln=1, align='C')
        pdf.set_font('DejaVu', '', 14)
        for i in range(0, len(questions)):
            pdf.set_font('DejaVu', '', 18)
            pdf.cell(200, 10, txt="Question", align='C')
            pdf.set_font('DejaVu', '', 14)
            pdf.write(8,"Q{}".format(i+1)+ questions[i])
            pdf.ln(8)
            pdf.set_font('DejaVu', '', 18)
            pdf.cell(200, 10, txt="Answer", align='C')
            pdf.set_font('DejaVu', '', 14)
            pdf.write(8, answers[i])
            pdf.ln(8)
        pdf.output("answers.pdf")
        with open("answers.pdf", "rb") as file:
            btn = st.download_button(
                label="Download Pdf",
                data=file,
                file_name="answers.pdf"
            )
    else:
        st.error("Fill all the fields")
