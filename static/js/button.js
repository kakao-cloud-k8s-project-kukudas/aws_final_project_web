
            $(document).ready(function() {
              $('#create_btn').click(function(e) {
                e.preventDefault()
                $.ajax({
                  url: '/run-long-task/',
                  type: 'POST',
                  data: {
                    l: 1,
                    csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
                  }
                })
                .done((response) => {
                  updateState(response.task_id)
                })
                .fail((error) => console.log(error))
              })

              $('#delete_btn').click(function(e) {
                e.preventDefault()

                $.ajax({
                  url: '/run-long-task/',
                  type: 'POST',
                  data: {
                    l: 2,
                    csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
                  }
                })
                .done((response) => {
                  updateState(response.task_id)
                })
                .fail((error) => console.log(error))
              })

              function updateState(taskID) {
                $.ajax({
                  url: `task-status/${taskID}/`,
                  type: 'GET'
                })
                .done(response => {
                  const data = `
                    <th>${response.task_id}</th>
                    <td>${response.state}</td>
                    <td>${response.progression}</td>
                    <td>${response.info}</td>
                    `
                  const tr = $('#' + response.task_id)
                  // if the element exists, update it
                  if (tr.length) {
                    tr.html(data)
                  }
                  // otherwise, create a new row in the table
                  else {
                    const tableBody = `<tr id='${response.task_id}'>${data}</tr>`
                    $('tbody').append(tableBody)
                  }

                  // response 조건 추가할 것
                  if (response.state == "SUCCESS" && response.info == "create") {
                    document.getElementById("create").innerText = "생성됨";
                    document.getElementById("delete_btn").removeAttribute("disabled");
                    document.getElementById("link").href = response.lb_address;
                  }
                  else if (response.state == "PROGRESS" && response.info == "create") {
                    document.getElementById("create").innerText = "생성중";
                    document.getElementById("create_btn").setAttribute('disabled', 'disabled');
                  }
                  else if (response.state == "SUCCESS" && response.info == "delete") {
                    document.getElementById("delete").innerText = "삭제됨";
                    document.getElementById("create_btn").removeAttribute("disabled");
//                    document.getElementById('link').disabled = true;
                  }
                  else if (response.state == "PROGRESS" && response.info == "delete") {
                    document.getElementById("delete").innerText = "삭제중";
                    document.getElementById("delete_btn").setAttribute('disabled', 'disabled');
                  }
//                  if (response.state == "FAILURE" || response.state == "SUCCESS") {return false}
                  // rerun every 2 seconds
                  setTimeout(function() {
                    updateState(response.task_id)
                  }, 3600)
                })
                .fail(error => console.log(error))
              }
            })