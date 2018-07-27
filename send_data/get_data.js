var count = 0;
var needToSendMail = false;
var messagesToSend = {
  dms: [],
  tasks:[],
  teams:[]
};

function populateMessagesToSend(entities, entityType,username) {
  if(entityType=='dms') {
    entities.forEach(function(entity) {
      entity.messages.forEach(function(message){
        if (!needToSendMail && inLastOneHour(message)) {
            needToSendMail=true
        }

        messagesToSend.dms.push(prepareMessage(entity, message,entityType))
        count++
      })
    })
  } else {
     entities.forEach(function(entity) {
      var userMentioned = false;
      var messages = [];
      
      if(entityType=='tasks') {
        messages.push('<b>#'+entity.teamName+'</b> ->' +entity.title)
      } else {
        messages.push('<b>#'+entity.name+'</b>')
      }
      
      entity.messages.forEach(function(message){
        if (!userMentioned && isUserMentioned(message, username)) {
          userMentioned = true;
        }

        if (!needToSendMail && userMentioned && inLastOneHour(message)) {
          needToSendMail=true
        }

        messages.push(prepareMessage(entity, message, entityType))

      })

      if (userMentioned && messages.length>1) {
        count--
        messages.forEach(function(msg){
          messagesToSend[entityType].push(msg)
          count++
        })
      }
    })
  }
}

function inLastOneHour(message)
{
  var messageTime=Math.floor((new Date(message.createdAt).getTime()/1000))
  //print(messageTime)
  var dateTime=Math.floor((new Date()).getTime()/1000)
 // print(dateTime)
  if(messageTime>=(dateTime-3600))
  {
    return true
  }

  return false
}

function prepareMessage(entity, message, entityType)
{
  var msg=''
  
  if(entityType=='dms') {
    msg+='<b><i>'+message.sender.firstName+':-</i></b> '+message["content"]
  } else {
    msg+='<i>@'+message.sender.firstName+'</i>:- '+message['content']
  }
  
  return msg
}

function isUserMentioned(message,username) {
var msg=message['content']
    msg=msg.replace(/[\n]/g,'')
    msg=msg.split(" ")
    for(var i=0;i<msg.length;i++)
    {
      msg[i]=msg[i].split('@')
      if(msg[i].length>1)
      {
        for(var j=0;j<msg[i].length;j++)
        {
          if(msg[i][j]==username)
          {
            return true
            break
          }
        }
      }
    }
}

function prepareMailContent() {
  if(needToSendMail & count > 0) {
    var mailContent = messagesToSend.dms.join('<br>')+'<br>'+messagesToSend.teams.join('<br>')+'<br>'+messagesToSend.tasks.join('<br>')
    mailContent = mailContent.replace(/[`]/g,' ').replace(/[\n]/g,' ').replace(/[\t]/g,' ')
    return mailContent
  }
}
populateMessagesToSend($dms,'dms',$username)
populateMessagesToSend($teams,'teams',$username)
populateMessagesToSend($tasks,'tasks',$username)
var result = {
  mailContent: prepareMailContent(),
  totalMessages: count,
  needToSendMail: needToSendMail
}
result;