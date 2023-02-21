document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  document.querySelector("#compose-form").onsubmit = () => {
    send_email(); 
    return false;
  }
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // console.log(emails);

      emails.forEach(email => {
        // console.log(email);
        const div = document.createElement('div');
        div.setAttribute("class", "row");
        div.setAttribute("id", "email-list");
        div.innerHTML = `
          <h4 class="col-4"><b>${email.sender}</b></h4>
          <h4 class="col-6">${email.subject}</h4>
          <h6 class="col-2">${email.timestamp}</h6>
        `;

        if (email.read) {
          div.style.backgroundColor = "gray";
        }
        else {
          div.style.backgroundColor = "white";
        }

        // console.log(email);
        div.addEventListener('click', () => {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              read: true
            })
          });
          // console.log(email);
          load_email(mailbox, email);
        })

        document.querySelector('#emails-view').append(div);
      });
    });
}

function load_email(mailbox, email) {
  // console.log(mailbox);
  // console.log(email);
  document.querySelector('#email-view').innerHTML = "";

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  const div = document.createElement('div');
  div.innerHTML = `
  <h4><b>From:</b> ${email.sender}</h4>
  <h4><b>To:</b> ${email.recipients}</h4>
  <h4><b>Subject:</b> ${email.subject}</h4>
  <h4><b>Timestamp:</b> ${email.timestamp}</h4>
  <button class="btn btn-sm btn-outline-primary" id="reply" onclick='reply(${email.id}); '>Reply</button>
  <hr>
  <h5>${email.body}</h5>
  `;
  document.querySelector('#email-view').append(div)

  
  if (mailbox === 'inbox') {
    const button = `
      <button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>
    `;
    div.innerHTML += button;

    document.querySelector('#archive').addEventListener('click', () => {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: true
        })
      }).then(() => {load_mailbox('inbox')})
    });
  }
  else if (mailbox === 'archive') {
    const button = `
      <button class="btn btn-sm btn-outline-primary" id="unarchive">Unarchive</button>
    `;
    div.innerHTML += button;

    document.querySelector('#unarchive').addEventListener('click', () => {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: false
        })
      }).then(() => {load_mailbox('inbox')})
    });
  }
}

function send_email() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector("#compose-recipients").value,
      subject: document.querySelector("#compose-subject").value,
      body: document.querySelector("#compose-body").value
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent'); 
  });
}

function reply(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      compose_email();

      console.log(email);

      let subject = "";
      if (email.subject.slice(0,2) === 'Re') {
        subject += email.subject;
      }
      else {
        subject += `Re: ${email.subject}`;
      }

      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
  });
}