var overs=document.getElementsByClassName('time-stamp');var ball=document.getElementsByClassName('over-score');var runs=0;var wickets=0; var ele={};for(i=overs.length-1;i>=0;i--){ ball[i].innerText.trim()==="W"?wickets++:wickets;if(ball[i].innerText.trim().includes("w")){b=Number(ball[i].innerText.trim()[0]);}else if(ball[i].innerText.trim().includes("b")){b=Number(ball[i].innerText.trim()[0]);}else if(ball[i].innerText.trim()==="W"){b=0;}else{b=ball[i].innerText.trim();}o=(overs[i].innerText.trim().includes(".6"))?Math.round(Number(overs[i].innerText.trim())):overs[i].innerText.trim();runs=Number(runs)+Number(b);ele[overs[i].innerText]=[Number(o), 2, wickets, runs]};