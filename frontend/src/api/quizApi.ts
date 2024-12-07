import axios from "axios";

async function getQuizzes() {
  const config = {
    headers: { Authorization: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiR0FudiIsImV4cCI6MTczMzYxMzczOX0.M7W8nqvwh7oPjDSOxZkoMcOW_TPiBSvgYm1nCSR14Hs` }
  };
  axios.get('https://localhost/api/latest/quizzes', config)
    .then(function (response) {
      // handle success
      console.log(response);
    })
    .catch(function (error) {
      // handle error
      console.log(error);
    })
    .finally(function () {
      // always executed
    });
}
