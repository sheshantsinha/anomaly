var new_msg=false,type_msg=false,str='',count=0
var new_date=Math.floor((new Date()).getTime()/1000)

function find_msg(msg_arr,new_date)
{
  if(msg_arr.length==0) return;
  msg_arr.forEach(function(item)
  {
    (item.messages).forEach(function(msg){
      var old_date=Math.floor((new Date(msg.createdAt)).getTime()/1000)
      if((new_date-old_date)<=3600 & (new_date-old_date)>=0)
      {
        new_msg=true
      }
    })
  })
}

function build_data(msg,bl)
{
  if(bl==0)
  {
    msg.forEach(function(packet){
      (packet.messages).forEach(function(pack2){
        str=str+"<b><i>"+(pack2.sender.firstName)+"</i></b>: "+(pack2.content)+"<br>"
        count++
      })
    })
    type_msg=true
  }
  if(bl==1)
  {
    msg.forEach(function(packet){
      str=str+"<br><b>#"+(packet.teamName)+"</b> -> "+(packet.title)+"<br>";
      (packet.messages).forEach(function(pack2){
        var mss=(pack2.content).split(" "),mentioned=false
        for (var i=0;i<mss.length;i++)
        {
          mss[i]=mss[i].split("@")
          if (mss[i].length>0)
          {
            for (var k=0;k<mss[i].length;k++)
            {
              if(mss[i][k]==$username)
              {
                mentioned=true
                type_msg=true
              }
            }
          }
        }
        if(mentioned==true)
        {
          str=str+"<i>@"+(pack2.sender.firstName)+"</i>: "+(pack2.content)+"<br>"
          count++
        }
      }) //
    })
  }
  if(bl==2)
  {
    msg.forEach(function(packet){
      str=str+"<br><b>#"+(packet.name)+"</b><br>";
      (packet.messages).forEach(function(pack2){

        var mss=(pack2.content).split(" "),mentioned=false
        for (var i=0;i<mss.length;i++)
        {
          mss[i]=mss[i].split("@")
          if (mss[i].length>0)
          {
            for (var k=0;k<mss[i].length;k++)
            {
              if(mss[i][k]==$username)
              {
                mentioned=true
                type_msg=true
              }
            }
          }
        }
        if(mentioned==true)
        {
          str=str+"<i>@"+(pack2.sender.firstName)+"</i>: "+(pack2.content)+"<br>"
          count++
        }
      })
    })
  }
}

function length_count(ele)
{
  temp_count=0
  for(var i=0;i<ele.length;i++)
  {
    temp_count+=(ele[i].messages).length
  }
  return temp_count
}



find_msg($tasks,new_date)
find_msg($dms,new_date)
find_msg($teams,new_date)


if(new_msg==true)
{
  str="Hey <b>"+$firstName+"</b>,<br>You have <b>"+count+"</b> unread messages on KISS.<br>"
  if($dms.length>0)
  {
    str=str+"<br><u><b>Direct Messages</b></u><br>"
    build_data($dms,0)
  }
  if($tasks.length>0)
  {
    str=str+"<br><u><b>Task</b></u>"
    build_data($tasks,1)
  }
  if($teams.length>0)
  {
    str=str+"<br><u><b>Team</b></u>"
    build_data($teams,2)
  }
}
str1=str.replace(/[`]/g,' ').replace(/[\n]/g,' ').replace(/[\t]/g,' ')
var data={str:str1,countx:count}
data;
