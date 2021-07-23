import React, { useRef, useState } from 'react'
import Typography from '@material-ui/core/Typography'
import Button from '@material-ui/core/Button'
import { Container, makeStyles } from '@material-ui/core'
import TextField from '@material-ui/core/TextField'


const useStyles = makeStyles({
  field: {
    marginTop: 20,
    marginBottom: 20,
    display: "block"
  }

})

export default function Notes() {
  const classes = useStyles()
  const [urlIn, setUrlIn] = useState('')
  const [urlOut, setUrlOut] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (urlIn) {
      console.log(urlIn)
      setUrlOut(urlIn)
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({url:urlIn})
      };
      fetch('http://localhost:5000', requestOptions)
        .then(response => response.json())
        .then(data => setUrlOut(data['new_url']))

    }

  }


  return (
    <div>
      <Container>
        <Typography
          variant="h1"
          color="textSecondary"
          align="center"
        >
          URL Shortener!
        </Typography>

        <form noValidate autoComplete="off" onSubmit={handleSubmit}>
          <TextField
            onChange={(e) => setUrlIn(e.target.value)}
            className={classes.field}
            label="Paste Your URL Here!"
            variant="outlined"
            fullWidth
            required
          />


          <Button
            onClick={() => console.log('ooooooooooooooooooooo')}
            type='submit'
            color='secondary'
            variant='contained'
          >
            Submit
          </Button>

        </form>

        {
          (urlOut !== '') ?
            <Typography
              variant="h4"
              color="textSecondary"
              align="center"
            >
              Shortened url below:
            </Typography> : null
        }






        <Typography
          variant='h2'
          align="center"
        >
          {urlOut}
        </Typography>

      </Container>
    </div>
  )
}
