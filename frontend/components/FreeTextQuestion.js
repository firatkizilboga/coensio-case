import { useState, useEffect } from "react"

export default function FreeTextQuestion(props) {
    const [answer, setAnswer] = useState(null)
    useEffect((e) => {
        props.onAnswerChange && props.onAnswerChange(question.id_in_exam, answer);
      }, [answer]);
    
      const handleTextAreaChange = (e) => {
        setAnswer(e.target.value);
      };
    
    const question = props.question
    return (
        <div className="bg-accent">
            <h2>
                {question.question}
            </h2>
                
            <textarea
                placeholder="Enter your answer here!"
                className="form-control"
                onChange={handleTextAreaChange}
            ></textarea>
        </div>
    )
}


