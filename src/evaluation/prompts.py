import os
from typing import List, Tuple

def text_oracle_instructions() -> str:
  return """
  We would like to generate a command to modify a HTML page. Here are the list of valid commands:
  self.modify_text(input_name: str, input_value)
  self.modify_checkbox(input_name: str, input_value)
  self.modify_radio(input_name: str, input_value)
  self.modify_select(input_name: str, input_value)
  self.modify_range(input_name: str, input_value)

  Here are a few examples:

  """

def text_vision_oracle_instructions() -> str:
  return """
  I am a system that generates a command to modify a HTML page. Here are the list of valid commands I will output:
  self.actions.modify_text(input_name: str, input_value)
  self.actions.modify_checkbox(input_name: str, input_value)
  self.actions.modify_radio(input_name: str, input_value)
  self.actions.modify_select(input_name: str, input_value)
  self.actions.modify_range(input_name: str, input_value)

  It is extremely important that before the specific method (modify_select, modify_range, etc.) you prepend self.actions.

  I expect to be given a specific input to modify, and the HTML code of the webpage, and a screenshot of the webpage. I will have to generate a command from the list above to modify the input. 
  """

def few_shot_examples() -> List[Tuple[str, str, str]]:
  """
  Returns a list of few-shot examples in their own array index of type [Input/HTML Code, Image Path, Output Line]

  Output Line Format:
  self.actions.modify_checkbox('q1-quant', 'nan')
  """

  instance_1 = [
    """
    Input name: q1-quant
    HTML: 
    <html><head>
        <title>Task</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        
      </head>
      <body>
        <form name="mturk_form" method="post" id="mturk_form" target="_parent" action="#">

          <input type="hidden" name="csrfmiddlewaretoken" value="4A65J4dKTRgvAhdZNYd1oZB4RV60Tq9aS8X6Jk5yEdvxvMub3oCaZRwdVgkLYVo3">
          <meta content="width=device-width,initial-scale=1" name="viewport">
    <section class="container" id="SurveyLink"><!-- Instructions -->
    <div class="row">
    <div class="col-xs-12 col-md-12">
    <div class="panel panel-primary"><!-- WARNING: the ids "collapseTrigger" and "instructionBody" are being used to enable expand/collapse feature --><a class="panel-heading" href="javascript:void(0);" id="collapseTrigger"><strong>&nbsp;()Question type definitions&nbsp;</strong></a>
    <div class="panel-body" id="instructionBody">
    <p dir="ltr" style="line-height: 1.38; margin-top: 0pt; margin-bottom: 8pt;"><span id="docs-internal-guid-f2f08346-7fff-f178-9f88-b169b26eb03c"><span style="font-size: 10pt; font-family: Arial; background-color: transparent; font-variant-numeric: normal; font-variant-east-asian: normal; vertical-align: baseline; white-space: pre-wrap;">Given a few English questions, we ask you to annotate each question with their corresponding type(s):</span></span></p>

    <ul dir="ltr">
      <li style="line-height: 1.38; margin-top: 0pt; margin-bottom: 8pt;"><strong>Question:</strong>&nbsp;When was the Dormition church destroyed?&nbsp; (Answer:&nbsp;1922)&nbsp;</li>
      <li style="line-height: 1.38; margin-top: 0pt; margin-bottom: 8pt;"><strong>Label:</strong>&nbsp;Date&nbsp;</li>
    </ul>

    <p style="line-height: 1.38; margin-top: 0pt; margin-bottom: 8pt;">Another example:&nbsp;</p>

    <ul>
      <li style="line-height: 1.38; margin-top: 0pt; margin-bottom: 8pt;"><strong>Question:&nbsp;</strong>&nbsp;Melbourne has sustained the highest population increase and economic growth rate in any Australian city according to what organization? (Answer:&nbsp;Australian Bureau of Statistics)&nbsp;</li>
      <li style="line-height: 1.38; margin-top: 0pt; margin-bottom: 8pt;"><strong>Label:</strong>&nbsp; Organization&nbsp;</li>
    </ul>

    <p dir="ltr" style="line-height: 1.38; margin-top: 0pt; margin-bottom: 8pt;">&nbsp;</p>

    <p dir="ltr" style="line-height: 1.38; margin-top: 0pt; margin-bottom: 8pt;"><span id="docs-internal-guid-f2f08346-7fff-f178-9f88-b169b26eb03c"><span style="font-size: 10pt; font-family: Arial; background-color: transparent; font-variant-numeric: normal; font-variant-east-asian: normal; vertical-align: baseline; white-space: pre-wrap;">Below we define and give examples for each label: </span></span></p>

    <ul>
      <li dir="ltr">
      <p dir="ltr"><strong>Humans:</strong> Any individual or group of humans, including fictional ones. Examples are: a group or organization of persons , an individual, title of a person, description of a person</p>
      </li>
      <li dir="ltr">
      <p dir="ltr"><strong>Event:</strong> &nbsp;Examples are: Named hurricanes, Battles, Wars, Sports events, Terrorist attacks</p>
      </li>
      <li dir="ltr">
      <p dir="ltr"><strong>Entity:</strong> &nbsp;A thing with distinct and independent existence. Examples are: Animals, Organs of body, Colors, Inventions, books and other creative pieces, Currency name, Diseases, and medicine, Food, Musical instrument, Languages, Plants, Products, Religions, Sports, Elements and substances, Symbols and signs, Techniques and methods, Equivalent terms, Vehicles</p>
      </li>
      <li dir="ltr">
      <p dir="ltr"><strong>Facility:</strong> Buildings, Airports, Highways, Bridges</p>
      </li>
      <li dir="ltr">
      <p dir="ltr"><strong>Location:</strong> Examples are: Cities, Countries, Mountains, States</p>
      </li>
      <li dir="ltr">
      <p dir="ltr"><strong>Law:</strong> Named documents made into laws; for example “the first amendment”</p>
      </li>
      <li dir="ltr">
      <p dir="ltr"><strong>Organization:</strong> an organized body of people with a particular purpose; examples are Company names (e.g. Google), Cults or terrorist groups (e.g. Al Qaeda),</p>
      </li>
      <li dir="ltr">
      <p dir="ltr"><strong>Date:</strong> Absolute or relative dates or periods, bigger than 1 day. Examples are Year (e.g. 1991), Range (e.g. from Monday to Tuesday, or during the 20th century), Approximate time (around 1880, or in the 70s)</p>
      </li>
      <li dir="ltr">
      <p dir="ltr"><strong>Time:</strong>&nbsp;Any temporal range/unit that is shorter than a day&nbsp;&nbsp;(e.g. 2 o'clock).&nbsp;</p>
      </li>
      <li dir="ltr">
      <p dir="ltr"><strong>Money:</strong> Monetary values, including unit; for example “$26”.</p>
      </li>
      <li dir="ltr">
      <p dir="ltr"><strong>Quantity:</strong> postcodes or other codes, the number of sth, Ranks, fractions, speed, temperature, size, area, and volume, weight</p>
      </li>
      <li dir="ltr">
      <p dir="ltr"><strong>Description:</strong> description and abstract concepts. Examples are: description and abstract concepts, the definition of sth., the manner of an action, reasons</p>
      </li>
      <li><strong>Abbreviation:</strong> expression abbreviated</li>
    </ul>
    </div>
    </div>
    </div>
    </div>

    <div class="row" id="workContent">
    <div class="col-xs-12 col-md-6 col-md-offset-3">
    <div class="form-group">&nbsp;
    <div dir="ltr" style="margin-left:0pt;">
    <table style="border: none; width: 468pt;">
      <colgroup>
        <col width="*">
      </colgroup>
      <tbody>
        <tr style="height:0pt">
          <td style="border-left:solid #000000 1pt;border-right:solid #000000 1pt;border-bottom:solid #000000 1pt;border-top:solid #000000 1pt;vertical-align:top;padding:5pt 5pt 5pt 5pt;">
          <p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:8pt;"><span id="docs-internal-guid-21b65afa-7fff-c2ce-e480-3ba277b3295f"><span style="font-size: 10pt; font-family: Arial; background-color: transparent; font-weight: 700; font-variant-numeric: normal; font-variant-east-asian: normal; vertical-align: baseline; white-space: pre-wrap;">Question 1: </span><span style="font-size: 10pt; font-family: Arial; background-color: transparent; font-variant-numeric: normal; font-variant-east-asian: normal; vertical-align: baseline; white-space: pre-wrap;">What are Kanye's religious beliefs? (Answer: Christian) </span></span></p>

          <p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:8pt;"><span id="docs-internal-guid-21b65afa-7fff-c2ce-e480-3ba277b3295f"><span style="font-size: 10pt; font-family: Arial; background-color: transparent; font-variant-numeric: normal; font-variant-east-asian: normal; vertical-align: baseline; white-space: pre-wrap;">Use your best judgment to select the "type"(s) that best describe the question: </span></span></p>
          <input name="q1-humans" type="checkbox" value="q1-humans"> Humans<br>
          <input name="q1-events" type="checkbox" value="q1-events"> Event<br>
          <input name="q1-entity" type="checkbox" value="q1-entity"> Entity<br>
          <input name="q1-facility" type="checkbox" value="q1-facility"> Facility<br>
          <input name="q1-location" type="checkbox" value="q1-location"> Location<br>
          <input name="q1-law" type="checkbox" value="q1-law"> Law<br>
          <input name="q1-org" type="checkbox" value="q1-org"> Organization<br>
          <input name="q1-date" type="checkbox" value="q1-date"> Date<br>
          <input name="q1-time" type="checkbox" value="q1-time"> Time<br>
          <input name="q1-money" type="checkbox" value="q1-money"> Money<br>
          <input name="q1-quant" type="checkbox" value="q1-quant"> Quantity<br>
          <input name="q1-desc" type="checkbox" value="1-desc" checked=""> Description<br>
          <input name="q1-abbrv" type="checkbox" value="q1-abbrv"> Abbreviation<br>
          <input name="q1-other" type="checkbox" value="q1-other"> Other</td>
        </tr>
      </tbody>
    </table>

    </section>
    <link crossorigin="anonymous" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" integrity="sha384-IS73LIqjtYesmURkDE9MXKbXqYA8rvKEp/ghicjem7Vc3mGRdQRptJSz60tvrB6+" rel="stylesheet">
    <style type="text/css">#collapseTrigger{ color:#fff; display: block; text-decoration: none; } #submitButton{ white-space: normal; } .image{ margin-bottom: 15px; } /* CSS for breaking long words/urls */ .dont-break-out { overflow-wrap: break-word; word-wrap: break-word; -ms-word-break: break-all; word-break: break-all; word-break: break-word; -ms-hyphens: auto; -moz-hyphens: auto; -webkit-hyphens: auto; hyphens: auto; }
    </style>

          
          <p class="text-center">
            <input type="submit" id="submitButton" class="btn btn-primary" disabled="" value="You must ACCEPT the Task before you can submit the results.">
          </p>
          
        </form>
      

    </body></html>
    """,
    os.path.join("img", "ex1.png"),
    "self.actions.modify_checkbox('q1-quant', 'nan')"
  ]

  instance_2 = [
    """
    Input name: 0-0
    HTML:
    <html><head>
        <title>Task</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

      </head>
      <body>
        <form name="mturk_form" method="post" id="mturk_form" target="_parent" action="#">

          <input type="hidden" name="csrfmiddlewaretoken" value="PdTCn5pFOkjXQ2Ry4bSa8nz9zxROgkX5hde2yFSw6LRRKER8aoUGowtMsVEs9SP7">
          <section class="container" id="Writing">
    <div class="row" id="workContent">
    <div class="row">
    <div class="col-xs-12 col-md-12">
    <div class="panel panel-primary" style="background-color:#F0F8FF; overflow: auto;"><!-- WARNING: the ids "collapseTrigger" and "instructionBody" are being used to enable expand/collapse feature --><a class="panel-heading" href="javascript:void(0);" id="collapseTrigger"><strong>Instructions</strong></a>
    <div class="panel-body" id="instructionBody">
    <h3>Answering a Reading Comprehension Task</h3>
    You are answering a reading comprehension test. You will read a <b>paragraph</b> and some <b>question</b>s, and a few <b>options</b> for its answer. You will have to choose the <b>correct</b> answer(s) from the options.<br>
    Note that sometimes, <span style="color: red">more than one option </span> can answer the question correctly and completely. In those cases, <span style="color: red">please select all such options</span>.<br>
    <br>
    <br>
    Here is an example:
    <div class="boxedBig">
    <h4>Paragraph:</h4>
    Obama was born on August 4, 1961, at KapiÊ»olani Maternity &amp; Gynecological Hospital in Honolulu, Hawaii.<br>
    He is the only President to have been born in Hawaii. He was born to a white mother and a black father. His mother, Ann Dunham (1942-1995), was born in Wichita, Kansas, of mostly English descent, with some German, Irish, Scottish, Swiss, and Welsh ancestry.</div>

    <div class="boxedBig"><b>Question: </b> How old was Obama's mother when he was born?

    <div class="form-group">
    <div class="col-lg-10"><label class="checkbox-inline"><input onclick="return false;" type="checkbox"> teenager </label><br>
    <label class="checkbox-inline"><input onclick="return false;" type="checkbox"> in his 40s </label><br>
    <label class="checkbox-inline"><input onclick="return false;" type="checkbox"> mid 20s </label><br>
    <label class="checkbox-inline"><input checked="checked" onclick="return false;" type="checkbox"> almost twenty </label></div>
    </div>
    <br>
    <br>
    <br>
    <br>
    <b>Explanation: </b> Obama was born in 1961. His mother was born in 1942 and 1961-1942=19. The good option (almost twenty) answers the question correctly. The bad answers give an incorrect answer.</div>

    <div class="boxedBig"><b>Question: </b> Where was Ann living in August, 1961?

    <div class="form-group">
    <div class="col-lg-10"><label class="checkbox-inline"><input onclick="return false;" type="checkbox"> KapiÊ»olani Maternity </label><br>
    <label class="checkbox-inline"><input checked="checked" onclick="return false;" type="checkbox"> Honolulu, Hawaii </label><br>
    <label class="checkbox-inline"><input onclick="return false;" type="checkbox"> Wichita </label><br>
    <label class="checkbox-inline"><input onclick="return false;" type="checkbox"> England </label><br>
    <label class="checkbox-inline"><input checked="checked" onclick="return false;" type="checkbox"> Honolulu </label></div>
    </div>
    <br>
    <br>
    <br>
    <br>
    <br>
    <b>Explanation: </b> Ann is Obama's mother (Sent 4). She must have been there when Obama was born (Sent 1). Obama was born in Hawaii (Sent 2). Hawaii is also in Honolulu. So both Hawaii and Honolulu answer the question correctly. Kansas and Scottland don't answer the question correctly.</div>
    </div>
    </div>
    </div>
    </div>

    <h4>For the following paragraph, select <u>all</u> the correct answer(s).</h4>

    <h4>There might be&nbsp;<span style="background-color: rgb(240, 248, 255); color: red;">more than one correct answer; </span><span style="background-color: rgb(240, 248, 255);">in which case,&nbsp;</span><span style="background-color: rgb(240, 248, 255); color: red;">please select <strong><u>all</u></strong>&nbsp;the options that&nbsp;apply to the question.&nbsp;</span></h4>

    <div id="userInputBox">
    <div class="boxedBig"><b>Paragraph: </b> <b>Sent 1: </b>Low-income domestic violence victims may find long-term legal help -- representation in divorces or child-custody disputes -- hard to come by, if two organizations now providing such help can't replace their lost funding.<br><b>Sent 2: </b>The Legal Aid Society of Salt Lake and Utah Legal Services are already facing cutbacks after they were refused a federal grant of more than $450,000 in September.<br><b>Sent 3: </b>The board overseeing the state Office of Crime Victim Reparations [CVR] has voted to deny a stopgap funding request from the two organizations.<br><b>Sent 4: </b>While describing the request as a worthy cause, board members agreed Tuesday that funding divorces or custody disputes was outside their focus -- providing direct services for crime victims.<br><b>Sent 5: </b>The $175,000 requested would have allowed the legal aid groups to maintain a skeleton staff to continue providing help beyond emergency protective orders for victims, completing existing cases and offering services in limited cases.<br><b>Sent 6: </b>The groups also plan to enlist more pro bono attorneys through coordination with the Utah State Bar. "We don't have a lot more options," said Anne Milne, executive director of Utah Legal Services, after learning of the CVR refusal Wednesday.<br><b>Sent 7: </b>The organization has already lost some staff through attrition and has turned away some cases, she said.<br><b>Sent 8: </b>Milne said she may ask the board overseeing her organization to give her until November to seek funding from additional sources.<br><b>Sent 9: </b>Without additional funding, the outlook for longer-term legal help is unclear.<br><b>Sent 10: </b>For two years, the groups had received 18-month civil legal assistance grants from the U.S. Department of Justice and had used them to provide such assistance.<br><b>Sent 11: </b>But last month, a third request was denied.<br><b>Sent 12: </b>Funding used to help victims obtain emergency protective orders remains in place, said Milne and Stewart Ralphs, executive director of the Legal Aid Society of Salt Lake.<br><b>Sent 13: </b>Although an order's requirements that an abuser stay away from a victim may remain in effect for years, protective orders only settle issues such as child custody, child support, custody and property arrangements for 150 days.<br><b>Sent 14: </b>Many judges are reluctant to address those issues in emergency protective orders, since the decrees stay in effect for such a short time, Milne and Ralphs said.<br><b>Sent 15: </b>"The likelihood a victim will return to her abuser increases if she cannot permanently sever the relationship and establish workable support, custody and property arrangements," the funding request to CVR said.<br><b>Sent 16: </b>The Department of Justice said it denied the grant application, in part, because evaluators did not see enough collaboration between the organizations and victims' advocates, Ralphs and Milne told CVR board members.<br><b>Sent 17: </b>While the two said they believe their organizations coordinate well, the organizations cannot appeal the grant denial.<br><b>Sent 18: </b>Although CVR board members considered giving the money as a loan, not a grant, their vote on the funding request -- taken after Milne and Ralphs left the meeting -- was unanimous.<br></div>
    <div class="boxedBig"><b>Question: </b> When a judge issues an emergency protective order is it long or short term and how many days does it cover?  &nbsp; &nbsp; &nbsp; &nbsp; <div class="form-group"><div class="col-lg-10"><label class="checkbox-inline"><input type="checkbox" name="0-0"> Emergency protective orders are short term and it lasts for a 150 days </label> &nbsp; &nbsp; &nbsp; &nbsp; <br><label class="checkbox-inline"><input type="checkbox" name="0-1"> These are shorter orders and stay for 150 days </label> &nbsp; &nbsp; &nbsp; &nbsp; <br><label class="checkbox-inline"><input type="checkbox" name="0-2"> Emergency protective orders are long term </label> &nbsp; &nbsp; &nbsp; &nbsp; <br><label class="checkbox-inline"><input type="checkbox" name="0-3"> Short term </label> &nbsp; &nbsp; &nbsp; &nbsp; <br></div></div> <br><br><br><br> </div></div>
    <input class="form-control" id="hiddenQuestion" name="hiddenName" type="text"><br>
    <br>
    &nbsp;</div>
    </section>
    <link crossorigin="anonymous" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" integrity="sha384-IS73LIqjtYesmURkDE9MXKbXqYA8rvKEp/ghicjem7Vc3mGRdQRptJSz60tvrB6+" rel="stylesheet">
    </style>


          <p class="text-center">
            <input type="submit" id="submitButton" class="btn btn-primary" disabled="" value="You must ACCEPT the Task before you can submit the results.">
          </p>

        </form>
    </body></html>
    """,
    os.path.join("img", "ex2.png"),
    "self.actions.modify_checkbox('0-0', 'on')"
  ]

  instance_3 = [
    """
    Input name: candidate2
    HTML: 
    <html><head>
        <title>Task</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    </head>
      <body>
        <form name="mturk_form" method="post" id="mturk_form" target="_parent" action="#">

          <input type="hidden" name="csrfmiddlewaretoken" value="PFhmO0bjOyyQHeDmq9u1QyEPaQBBXbgp0qs8SO4mQ1vPssyo18IOLMilnq5XpizB">
          <!-- You must include this JavaScript file -->
    <script data-loader="crowd-html-elements" src="https://assets.crowd.aws/vendor/webcomponentsjs/custom-elements-es5-adapter.js"></script><script data-loader="crowd-html-elements" src="https://assets.crowd.aws/vendor/web-animations-js/web-animations-next-lite.min.js"></script><script data-loader="crowd-html-elements" src="https://assets.crowd.aws/vendor/webcomponentsjs/webcomponents-bundle.js"></script><link href="https://assets.crowd.aws/css/crowd.css" rel="stylesheet"><script data-loader="crowd-html-elements" src="https://assets.crowd.aws/crowd-html-elements-without-ce-polyfill.js"></script><script src="https://assets.crowd.aws/crowd-html-elements.js"></script>

    <!-- For the full list of available Crowd HTML Elements and their input/output documentation,
          please refer to https://docs.aws.amazon.com/sagemaker/latest/dg/sms-ui-template-reference.html -->

    <!-- You must include crowd-form so that your task submits answers to MTurk -->
    <crowd-form answer-format="flatten-objects"><form method="" action="">
      <h1>Infer actions to accomplish a goal</h1>
      <p>
          In this task, we ask you to infer actions to accomplish a given goal.
          We will provide a <b>goal</b>, and some <b>actions</b> that may or may not help accomplish this goal.
          Your task is to choose <b>the most likely action that helps accomplish this goal</b>.
          </p><ul>
            <li>If multiple options seem equally likely, you have to choose one, but don't worry too much about it.</li>
            <li>Answer according to your common sense, but not necessarily what you would <i>personally</i> do.</li>
            <li>If the actions or goals are hard to understand, do your best to answer.</li>
            <li>You are encouraged to look up words you don't understand.</li>
          </ul>
          <a href="javascript:;" onmousedown="if(document.getElementById('example').style.display == 'none'){ document.getElementById('example').style.display = 'block'; }else{ document.getElementById('example').style.display = 'none'; }"> (show/hide an example)</a>
          <div id="example" style="display:none; border:3px; border-style:solid; border-color:#003399; padding: 1em;">
              <p>Goal: <b>Throw a baseball farther</b>.</p>
              <p>Which action is the most likely to help accomplish the goal?</p>
              <div class="col-md-4">
                <div class="radio">
                  <label for="radios-0">
                    <input type="radio" name="example1">
                    <b>Hold the piece of white cardboard in your hand</b>
                  </label>
                </div>
                <div class="radio">
                  <label for="radios-1">
                    <input type="radio" name="example1">
                    <b>Make an open bridge with your other hand</b>
                  </label>
                </div>
                <div class="radio">
                  <label for="radios-2">
                    <input type="radio" name="example1">
                    <b>Develop chemistry with your baseball teammates</b>
                  </label>
                </div>
                <div class="radio">
                  <label for="radios-1">
                    <input type="radio" name="example1" checked="checked">
                    <b>Hold the ball against your chest</b>
                  </label>
                </div>
                <div class="radio">
                  <label for="radios-1">
                    <input type="radio" name="example1">
                    None of the above is likely
                  </label>
                </div>
              </div>
              <p><u>Reason: It is very likely a beginning step when aiming at your target in throwing a baseball. The other actions are unlikely to help with the goal.</u></p>
          </div>
      <p></p>
      <p>This HIT has 10 tasks. You should spend around 20 seconds on each task, and 5 minutes on this HIT, with an hourly rate of 10 dollars. Hint: To answer faster, you can use <strong>(Shift+)Tab</strong> to jump back and forth between candidates and use <strong>Space</strong> to select. </p>
      <div style="display: none;">
        3
      </div>

      <div style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
          <p>Goal #1: <b>Avoid Holiday Office Party Blunders</b> </p>
      </div>
      <p>Which action is the most likely to help accomplish the goal?</p>
      <div class="col-md-4">
        <div class="radio">
          <label for="radios-0">
            <input type="radio" name="candidate1" value="1" required="">
            <b>Think about the lyrics you are singing and how they make you feel.</b>
          </label>
        </div>
        <div class="radio">
          <label for="radios-1">
            <input type="radio" name="candidate1" value="2" required="" checked="">
            <b>Never Make Assumptions About Who You Are Talking To</b>
          </label>
        </div>
        <div class="radio">
          <label for="radios-2">
            <input type="radio" name="candidate1" value="3" required="">
            <b>Use bullet points for your script.</b>
          </label>
        </div>
        <div class="radio">
          <label for="radios-1">
            <input type="radio" name="candidate1" value="4" required="">
            <b>Find common ground regularly during the discussion.</b>
          </label>
        </div>
        <div class="radio">
          <label for="radios-1">
            <input type="radio" name="candidate1" value="X" required="">
            None of the above is likely
          </label>
        </div>
      </div>

    <!--
      <p>Please rate your level of confidence about the previous answers:</p>
      Not confident at all<div id='slider'><crowd-slider name="confidence1" min="1" max="3" value="2" required pin></crowd-slider></div>Very confident
    -->

      <p>(optional) If there are any of the following problems with the texts, please check the corresponding boxes:</p>
      <div><crowd-checkbox name="grammar1" role="checkbox" tabindex="0" toggles="" aria-checked="false" aria-disabled="false" dir="null" style="--paper-checkbox-ink-size: 48px;"> Some texts don't make sense or aren't grammatical. </crowd-checkbox></div>
      <div><crowd-checkbox name="noidea1" role="checkbox" tabindex="0" toggles="" aria-checked="false" aria-disabled="false" dir="null" style="--paper-checkbox-ink-size: 48px;"> I have no idea what the given goal or actions means. </crowd-checkbox></div>
      <br>

    <!--
      <p>(optional) For other problems, comments or concerns, please describe briefly:</p>
      <crowd-input name="problems1" placeholder="Describe problems, if any..."></crowd-input>
      <div style="display: none;">
        1
      </div>
    -->
      <div style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
          <p>Goal #2: <b>Remove Old Carpeting</b> </p>
      </div>
      <p>Which action is the most likely to help accomplish the goal?</p>
      <div class="col-md-4">
        <div class="radio">
          <label for="radios-0">
            <input type="radio" name="candidate2" value="1" required="">
            <b>Sew the pieces together using the following method until you have a binding strip long enough to outline the perimeter of your quilt:</b>
          </label>
        </div>
        <div class="radio">
          <label for="radios-1">
            <input type="radio" name="candidate2" value="2" required="">
            <b>Cut the excess fabric off using fabric scissors, using the line you drew as a guide.</b>
          </label>
        </div>
        <div class="radio">
          <label for="radios-2">
            <input type="radio" name="candidate2" value="3" required="">
            <b>Cover the object with the liquid using your coated paint brush.</b>
          </label>
        </div>
        <div class="radio">
          <label for="radios-1">
            <input type="radio" name="candidate2" value="4" required="">
            <b>Use the pry bar to work under the carpet.</b>
          </label>
        </div>
        <div class="radio">
          <label for="radios-1">
            <input type="radio" name="candidate2" value="X" required="">
            None of the above is likely
          </label>
        </div>
      </div>

    <!--
      <p>Please rate your level of confidence about the previous answers:</p>
      Not confident at all<div id='slider'><crowd-slider name="confidence2" min="1" max="3" value="2" required pin></crowd-slider></div>Very confident
    -->

    <crowd-button form-action="submit" variant="primary" data-testid="crowd-submit">Submit</crowd-button></form></crowd-form>


          <p class="text-center">
            <input type="submit" id="submitButton" class="btn btn-primary" disabled="" value="You must ACCEPT the Task before you can submit the results.">
          </p>

        </form>
    </body></html>
    """,
    os.path.join("img", "ex3.png"),
    "self.actions.modify_radio('candidate2', '4')"
  ]

  return [instance_1, instance_2, instance_3]

def current_instance(input_name: str, html_code: str) -> str:
  return f"""
  Given the above examples, generate a command that solves the following instance. Note, generate only a single command, without any explanations.

  Input name: {input_name}
  HTML: {html_code}
  Output command:
  """

def get_encoded_input_prompt(input_name: str, html_code: str = None):
  ret = text_oracle_instructions()
  for idx, instance in enumerate(few_shot_examples()):
     ret += f"""
     ======
     Instance {idx}:
     {instance[0]}
     
     Output command: {instance[2]}
     """
    
  ret += current_instance(input_name, html_code)

  return ret