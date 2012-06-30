import flask,flask.views
import twitter
import os
from decimal import *
import datetime
from datetime import date
import re
app=flask.Flask(__name__)
app.secret_key="twitter_secret"

class View(flask.views.MethodView):
    def get(self):
        return flask.render_template("hpage.html")
    def post(self):
        username=flask.request.form["username"]
        api = twitter.Api()
	sts = api.GetUserTimeline(username)
	str1='none'
        for user2 in sts:
    	    user_name=user2.user.name
            user_follower=user2.user.followers_count
            user_friend=user2.user.friends_count
            user_status=user2.user.statuses_count
            user_date=user2.created_at   
            relative_date=user2.relative_created_at
            text_color=user2.user.profile_text_color
            text_bk_color=user2.user.profile_background_color
            break
#***************************************************
        user_name=user2.user.name
        user_screen_name=user2.user.screen_name
        user_fvrt=user2.user.favourites_count
        user_follower=user2.user.followers_count
        user_friend=user2.user.friends_count
        user_status=user2.user.statuses_count
        user_date=user2.created_at   
        relative_date=user2.relative_created_at
        text_color=user2.user.profile_text_color
        text_bk_color=user2.user.profile_background_color
#********************************************************        
        flask.flash("NAME :"+str(user_screen_name))
	flask.flash("USER NAME :"+str(user_name))
        flask.flash("TWEETS :"+str(user_status))
        flask.flash("FOLLOWING :"+str(user_friend))
        flask.flash("FOLLOWERS :"+str(user_follower))
#***********************************************************
#CALCULATING SCORE
        ratiorating=0.0
        ffratio_score=0
        if user_friend!=0:     #ratio 50 marks
           ratiorating=Decimal(user_follower)/Decimal(user_friend)
        else:
            ratiorating=1
        if Decimal(ratiorating)<Decimal('1') :
            ffratio_score=50*Decimal(ratiorating)
        else:
            ffratio_score=50
        score=ffratio_score 
        flask.flash(str(int(ffratio_score))+"/50")
        if user_status>50:    #status 10 marks
           status_score=10
        else:
             status_score=int((Decimal(user_status)/Decimal('50'))*10)
        score=score+status_score 
        flask.flash(str(int(status_score))+"/10")
        if user_fvrt>100:    #favouscore 10 marks    
           fvrt_score=10
        else:
             fvrt_score=int((Decimal(user_fvrt)/Decimal('100'))*10)
        score=score+fvrt_score 
        flask.flash(str(int(fvrt_score))+"/10")
     
        if str(user2.user.profile_background_color)!='none' :   #bk_color 5 marks
           bgcolor_score=int(5)                             
        score=score+bgcolor_score       
        flask.flash(str(int(bgcolor_score))+"/5")
        if str(user2.user.profile_text_color)!='none' :    #text_color 5 marks
           profilecolor_score=int(5)
        score=score+profilecolor_score
        flask.flash(str(int(profilecolor_score))+"/5")
	des_score=0
        if str(user2.user.description)!=str(''):   #description  5 marks
           des_score=int(5)
        score=score+des_score 
        flask.flash(str(int(des_score))+"/5")
        protection_score=0
        if str(user2.user.protected)=='false':   #protection 5 marks
           protection_score=int(5) 
        score=score+protection_score
        flask.flash(str(int(protection_score))+"/5")
        image_score=0
        if str(user2.user.profile_image_url)!='none': #image_url 5 marks
           image_score=int(5)
        score=score+image_score 
        flask.flash(str(int(image_score))+"/5")
        lc_score=0
        if int(user2.user.listed_count)>0:    #listed_count 5 marks
           lc_score=int(5)
        score=score+lc_score 
        flask.flash(str(int(lc_score))+"/5")
        flask.flash(str(int(score)))
#*******************************************************************     
        now = datetime.date.today()     #age 
        result = re.findall('[0-9]+', str(user2.user.created_at))
        n=0
        for i in result:
            if n==0:
               day=i 
            if n==5:
               year=i 
            n=n+1
        result_str = re.findall('[A-z]+', str(user2.user.created_at))
        n=0
        for i in result_str:
            if n==1:
               month=i
               break
            n=n+1
#**********************************************
        months_choices = []
        for i in range(1,13):
            months_choices.append((datetime.date(2008, i, 1).strftime('%B')))
            k=0
        for s in enumerate(months_choices):
            mn=str(s)
            k=k+1
            if mn.find(month)>=1:
               month=k 
               break            
        d0 = date(int(year), int(month), int(day))
        delta = d0 - now
        duration=int(int(-delta.days)/30)
        flask.flash(str(duration))  
#*****************************************************
        x=0 
        if duration!=0:           
           x=int(score/duration)
           y=100-score
           while x>y:
                 x=x-y
           score=score+x
        flask.flash(str(x))
        flask.flash(str(int(score))+"/100")
#*****************************************************
        #flask.flash("PROFILE CREATION DATE::"+str(user2.user.created_at))
        #flask.flash("CURRENT DATE::"+str(now))
        return self.hello()
    def hello(self):
        return flask.render_template("home_page.html")      
app.add_url_rule("/",view_func=View.as_view("main"), methods=['GET','POST','hello'])
app.debug = True
app.run()
