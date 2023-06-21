import Head from 'next/head'
import { useRef, useState } from 'react'
import Loader from '../components/Loader'
import MultipleChoiceQuestion from '../components/MultipleChoiceQuestion';
import FreeTextQuestion from '../components/FreeTextQuestion';

export default function Home() {
  const input_ref = useRef();
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState();
  const [examId, setExamId] = useState();
  const [error, setError] = useState();
  const [answers, setAnswers] = useState({});
  const [score, setScore] = useState();

  const handleAnswerChange = (questionId, answerValue) => {
    setAnswers((prev) => ({ ...prev, [questionId]: answerValue }));
  };

  const showResults = () => {
    console.log("User Answers:", answers);
  };

  
  return (
    <div >
      <Head>
        <title>Test Maker</title>
        <meta name="description" content="Coens.io case project!" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className='p-5'>
          <h1>Test Maker</h1>
          <div className='bg-accent'>
            <div className='d-flex'>
            <input ref={input_ref} type='text' className='form-control' placeholder='Enter a position!' />
            <button className='btn primary'
              onClick={
                async () => {
                  setLoading(true);
                  setQuestions(null);
                  setAnswers({});
                  alert('Loading...', loading);
                  
                  fetch('/api/profession', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                      profession: input_ref.current.value
                    })
                    
                  }
                  )
                  
                  .then((response) => 
                  {
                    if (!response.ok) {
                      setLoading(false);
                      alert('Process failed! Please try again!');
                    }
                    return response.json()
                  }
                  )
                  .then(data => {
                    setLoading(false);
                    setQuestions(data.exam);
                    setExamId(data.exam_id);
                  }
                  )
                }
              }
              > 
              GO!
            </button>
          </div>
          <br/>
          <p className='col'>This might take a couple minutes!</p>

              </div>
          <div className='align-items-center justify-content-center d-flex'>
            {loading ? (<div className='row'><Loader /> </div>)  : null}
          </div>
          <div className='d-flex flex-column'>
            {
              questions ? questions.map((question, index) => {
                if (question.is_multiple_choice) {
                  return <MultipleChoiceQuestion key={index} question={question} onAnswerChange={handleAnswerChange}/>
                }
                else if (question.is_free_text) {
                  return <FreeTextQuestion key={index} question={question} onAnswerChange={handleAnswerChange}/>
                }
              }
              ) : null
            }
            {
              
            }
          </div>
          {
            questions ? (<div className='bg-accent'>
            <div className='d-flex'>
            <p className='col'>This might take a couple minutes!</p>
            <p className='col'>{score ? <span>Your Score:</span>:null} {score}</p>
            <button className='btn primary'
              onClick={
                async () => {
                  await fetch('/api/getResults', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                      answers: answers,
                      exam_id: examId
                    })}).then((response) => {
                      return response.json()
                    }
                    ).then
                    (data => {
                      setScore(data.score);
                    })

                }}
              > 
              SUBMIT!
            </button>
          </div>
              </div>)
              : null
          }
          
      </main>
    </div>
  )
}
