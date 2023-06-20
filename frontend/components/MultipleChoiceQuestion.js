import { useState, useEffect } from "react"

export default function MultipleChoiceQuestion(props) {
    const [answer, setAnswer] = useState(null)
    useEffect(() => {
        props.onAnswerChange && props.onAnswerChange(question.id_in_exam, answer);
      }, [answer]);

    const question = props.question
    return (
        <div className="bg-accent">
            <h2>
                {question.question}
            </h2>
            <form>
                <div className="row">
                    <input className="col-1 mcq" type="radio" onClick={
                        () => {
                            setAnswer('a')
                        }
                    } id={question.id_in_exam} name={question.id_in_exam} />
                    <label for={question.id_in_exam} className="col">a) {question.a}</label>
                </div>

                <div className="row">

                    <input className="col-1 mcq" type="radio" onClick={
                        () => {
                            setAnswer('b')
                        }
                    } id={question.id_in_exam} name={question.id_in_exam} />
                    <label className="col" for={question.id_in_exam}>b) {question.b}</label>
                </div>
                <div className="row">

                    <input className="col-1 mcq" type="radio" onClick={
                        () => {
                            setAnswer('c')
                        }
                    } id={question.id_in_exam} name={question.id_in_exam} />
                    <label className="col" for={question.id_in_exam}>c) {question.c}</label>
                </div>
                <div className="row">

                    <input className="col-1 mcq" type="radio" onClick={
                        () => {
                            setAnswer('d')
                        }
                    } id={question.id_in_exam} name={question.id_in_exam} />
                    <label className="col" for={question.id_in_exam}>d) {question.d}</label>
                </div>
                </form>
            </div>

    )
}


