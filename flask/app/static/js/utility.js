// google.accounts.id.revoke('user@google.com', done => {
//     console.log('consent revoked');
// });

//for ajax time
function calculateTime(){
    $.getJSON('/api', function(data) {
            // Handle the JSON data here
            calTime(data)
        });

        function calTime(data){
            var date = new Date();
            var offset = date.getTimezoneOffset()
            offset = (offset/60)
            for(let i=0; i<data.length; i++){
            //get data from server
            let created_at =(data[i]["created_at"])
            created_at = created_at.split(" ")[1]
            created_at = created_at.split(':')
            let hour_created = Number(created_at[0])
            //for created_at
            if(offset < 0){
                //ahead GMT
                hour_created += Math.abs(offset)
                if(hour_created > 24){
                hour_created = hour_created - 24;
                }
            }else{
                //behind GMT
                hour_created -= offset
                if(hour_created < 0){
                hour_created = 24 - hour_created;
                }
            }
            created_at[0] = String(hour_created)
            created_at = created_at.join(':')
            let created_id = "postC-at-" + data[i]["id"];
            let update_id = "postU-at-" + data[i]["id"];
            //console.log(created_id,created_at)
            created_at = created_at.substring(0, 5)
            if(document.getElementById(created_id) == null){
                continue
            }
            document.getElementById(created_id).innerText = created_at;

            //for edited_at
            if(data[i]["edited_at"] != null){
                let edited_at =(data[i]["edited_at"])
                edited_at = edited_at.split(" ")[1]
                edited_at = edited_at.split(':')
                let hour_updated = Number(edited_at[0])
                if(offset < 0){
                //ahead GMT
                hour_updated += Math.abs(offset)
                if(hour_updated > 24){
                    hour_updated = hour_updated - 24;
                }
                }else{
                //behind GMT
                hour_updated -= offset
                if(hour_updated < 0){
                    hour_updated = 24 - hour_updated;
                }
                }
                edited_at[0] = String(hour_updated)
                edited_at = edited_at.join(':')
                edited_at = edited_at.substring(0, 5)
                if(document.getElementById(update_id) == null){
                    continue
                }
                document.getElementById(update_id).innerText = edited_at;
            }
            }
        }
}

// for refresh webtime
$.getJSON('/api', function(data) {
        // Handle the JSON data here
        calTime(data)
    });

    function calTime(data){
        var date = new Date();
        var offset = date.getTimezoneOffset()
        offset = (offset/60)
        for(let i=0; i<data.length; i++){
        //get data from server
        let created_at =(data[i]["created_at"])
        created_at = created_at.split(" ")[1]
        created_at = created_at.split(':')
        let hour_created = Number(created_at[0])
        //for created_at
        if(offset < 0){
            //ahead GMT
            hour_created += Math.abs(offset)
            if(hour_created > 24){
            hour_created = hour_created - 24;
            }
        }else{
            //behind GMT
            hour_created -= offset
            if(hour_created < 0){
            hour_created = 24 - hour_created;
            }
        }
        created_at[0] = String(hour_created)
        created_at = created_at.join(':')
        let created_id = "postC-at-" + data[i]["id"];
        let update_id = "postU-at-" + data[i]["id"];
        //console.log(created_id,created_at)
        created_at = created_at.substring(0, 5)
        console.log(created_at, created_id)
        if(document.getElementById(created_id) == null){
            continue
        }
        document.getElementById(created_id).innerText = created_at;

        //for edited_at
        if(data[i]["edited_at"] != null){
            let edited_at =(data[i]["edited_at"])
            edited_at = edited_at.split(" ")[1]
            edited_at = edited_at.split(':')
            let hour_updated = Number(edited_at[0])
            if(offset < 0){
            //ahead GMT
            hour_updated += Math.abs(offset)
            if(hour_updated > 24){
                hour_updated = hour_updated - 24;
            }
            }else{
            //behind GMT
            hour_updated -= offset
            if(hour_updated < 0){
                hour_updated = 24 - hour_updated;
            }
            }
            edited_at[0] = String(hour_updated)
            edited_at = edited_at.join(':')
            edited_at = edited_at.substring(0, 5)
            if(document.getElementById(update_id) == null){
                continue
            }
            document.getElementById(update_id).innerText = edited_at;
        }
        }
    }

function refresh(url=null,formData) {
//this function go to url /board and get the return html
//which has the lastest update feed
$.ajax({
    url: '/board',
    method: 'GET',
    success: function(callbackData) {
        const parsedHTMLData = $.parseHTML(callbackData);
        const feedbox = $(parsedHTMLData).find('#feed-box')
        $('#feed-box').html(feedbox.html())
        calculateTime(); //from utility.js
        dropdownFunction(); //from board.js
        popupFunction();//from popup.js
        editPost();//from popup.js

        //if refresh after delete show undo-delete button
        if(url == "board/delete"){
            $('.undo-delete').show();
            console.log("inif")
        }
        $('.undo-text').click(function(){
            let post_id = formData['id']
            unDelete(post_id)
        })
    },
    error: function(xhr, status, error) {
        // Handle error
        console.error(error);
    }
    });  
}

function refreshprofile(url=null,formData) {
    //this function go to url /board and get the return html
    //which has the lastest update feed
    $.ajax({
        url: '/board',
        method: 'GET',
        success: function(callbackData) {
            const parsedHTMLData = $.parseHTML(callbackData);
            const feedbox = $(parsedHTMLData).find('#feed-box')
            $('#feed-box').html(feedbox.html())
            calculateTime(); //from utility.js
            dropdownFunction(); //from board.js

    
            //if refresh after delete show undo-delete button
            if(url == "board/delete"){
                $('.undo-delete').show();
                console.log("inif")
            }
            $('.undo-text').click(function(){
                let post_id = formData['id']
                unDelete(post_id)
            })
        },
        error: function(xhr, status, error) {
            // Handle error
            console.error(error);
        }
        });  
    }
