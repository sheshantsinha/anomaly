a="dfhui @sheshant @pus how are you? @samar@manas"
a=a.split(" ")
for (var i=0;i<a.length;i++)
{
	a[i]=a[i].split("@")
	if(a[i].length>1)
	{
	for (var k=0;k<a[i].length;k++)
	{
		if(a[i][k]=='manas')
		{
			console.log(true)
		}
	}
	}
}
console.log(a)