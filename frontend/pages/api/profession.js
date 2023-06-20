// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

export default async function handler(req, res) {




 await fetch('http://127.0.0.1:8003/api/exam/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        profession: req.body.profession
    })
}).then(response => {
    if (!response.ok) {
        res.status(500).json({ error: 'Bad request' })
    }
    return response.json()
}
    )
.then(data => {
    console.log(data)
    res.status(200).json(data)
    
}
)

  
}
  