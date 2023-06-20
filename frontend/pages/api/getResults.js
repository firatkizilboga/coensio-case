// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

export default async function handler(req, res) {





    await fetch('http://127.0.0.1:8003/api/getResults/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            answers: req.body.answers,
            exam_id: req.body.exam_id
        })
    }).then(response => response.json())
        .then(data => {
            console.log(data)
            res.status(200).json(data)
        }
        )

}

