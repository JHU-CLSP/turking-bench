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

  instance_4 = [
    """
Input name: weakener_rationale1_relevant
HTML:
<html><head>
    <title>Task</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
  </head>
  <body>
    <form name="mturk_form" method="post" id="mturk_form" target="_parent" action="#">

      <input type="hidden" name="csrfmiddlewaretoken" value="dIgBz9HlLYf3Pkdh8LxB5wP4m1VZ2rFAbPwxM66vqlHocDUIZO9fzIVDzMTqYgc4">
      <meta content="width=device-width, initial-scale=1, shrink-to-fit=no" name="viewport">
<meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><!-- BOOTSTRAP CSS -->
<link crossorigin="anonymous" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" rel="stylesheet"><!-- HITPUB CSS -->
<link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i,700,700i" rel="stylesheet">
<style id="hitpub_css" type="text/css">/***********************************************
                        MOSAIC BOOTSTRAP OVERWRITES
                        ***********************************************/
                        #hitinfo .card {
                            border-radius: 0;
                        }
                        /*#hitinfo .card:first-child {
                            border-bottom: 0;
                        }*/
                         #hitinfo button.btn-link {
                            color: #fff;
                            text-decoration: none;
                         }
                        #hitinfo button.btn-link:hover {
                            text-decoration: none;
                        }
                        #hit ul.question-choice {
                            list-style-type: none;
                        }
                        .question .card {
                            border: none;
                            padding: 0;
                            background-color: inherit;
                        }
                        .question .choice-collapse {
                            margin-top: .5rem;
                        }
                        #hit div.choice-collapse {
                            display: inline-block;
                        }
                        #hit .container {
                            background-color: #fbfbfb;
                        }
                        /***********************************************
                        MOSAIC GENERAL STYLING
                        ***********************************************/
                        body {
                            font-family: "Open Sans", "Roboto", sans-serif;
                            line-height: 1.25;
                        }
                        textarea#feedback {
                            width: 100%
                        }
                        input#submitButton {
                            margin: auto;
                            display: block;
                            background-color: #2172a4;
                            color: #fff;
                            font-size: 1.125rem;
                            padding: .5rem 1rem;
                            cursor: pointer;
                            border-radius: 1rem;
                        }
                        input#submitButton:hover {
                            background-color: #06486F;
                        }
                        table, th, td {
                            border: solid 1px #ccc;
                        }
                        th, td {
                            padding: 1rem;
                        }
                        .noselect {
                            -webkit-touch-callout: none; /* iOS Safari */
                              -webkit-user-select: none; /* Safari */
                               -khtml-user-select: none; /* Konqueror HTML */
                                 -moz-user-select: none; /* Firefox */
                                  -ms-user-select: none; /* Internet Explorer/Edge */
                                      user-select: none; /* Non-prefixed version, currently
                                                            supported by Chrome and Opera */
                        }


                        /***********************************************
                        HIT CUSTOM STYLING
                        ***********************************************/
                        div.card-header {
                            background-color: #06486F;
                        }
                        div.card-header h5 {
                            color: #fff !important;
                        }

                        div.special-info {
                            color: #fff !important;
                            background-color:red !important;
                        }

                        .fill_in_blank input {
                            background-color: inherit;
                        }

                        .fill_in_blank input:focus {
                            outline: none;
                        }

                        .key-term {
                            font-weight: bold;
                            text-transform: uppercase;
                        }

                        .key-term2 {
                            font-weight: bold;
                            font-style: italic;
                        }

                        .premise {
                            color: purple;
                        }

                        .hypothesis {
                            color: blue;
                        }

                        .weakener {
                            color:red;
                        }

                        .strengthener {
                            color:green;
                        }
                        .rationale {
                            color:orange;
                        }

                        .inline-blank {
                            background-color: white;
                        }

                        tr.table-bad {
                            background-color:#fff7f6;
                        }

                        tr.table-good {
                            background-color:#f7fff6;
                        }


                        div.question{
                            border-bottom: 1px solid rgba(0,0,0,.125);
                        }

                        div.question span.required {
                            font-style: italic;
                        }


                        label[for="2"] {
                            background-color: #bbda9a !important;
                            color:#636363;
                        }
                        label[for="1"] {
                            background-color: #d8eac5 !important;
                            color:#636363;
                        }
                        label[for="0"] {
                            background-color: #cecece !important;
                            color:#636363;
                        }
                        label[for="-1"] {
                            background-color:  #fde9e9 !important;
                            color:#636363;
                        }
                        label[for="-2"] {
                            background-color: #f9c5c5 !important;
                            color:#636363;
                        }
                        label[for="-9"] {
                            background-color: #dfdfff !important;
                            color:#636363;
                        }

                        label[for="2"]:hover, label[for="2"].active {
                            background-color: #598b00 !important;
                        }
                        label[for="1"]:hover, label[for="1"].active {
                            background-color: #71b300 !important;
                        }
                        label[for="0"]:hover, label[for="0"].active {
                            background-color: #555555 !important;
                        }
                        label[for="-1"]:hover, label[for="-1"].active {
                            background-color:  #ea0000 !important;
                        }
                        label[for="-2"]:hover, label[for="-2"].active {
                            background-color: #c90000 !important;
                        }

                        label[for="-9"]:hover, label[for="-9"].active {
                            background-color: #0000f9 !important;
                        }

                        .text2 {
                            color: #406400;
                            font-weight: bold;
                        }
                        .text1 {
                            color: #598b00;
                            font-weight: bold;
                        }
                        .text0 {
                            color: #555555;
                            font-weight: bold;
                        }
                        .text-1 {
                            color: #f90000;
                            font-weight: bold;
                        }
                        .text-2 {
                            color: #c90000;
                            font-weight: bold;
                        }
                        .text-9 {
                            color: #000093;
                            font-weight: bold;
                        }

                        .custom-disable {
                            pointer-events: none;

                        }

                        /* Arrows by westonganger/bootstrap-directional-buttons */
                        .btn-arrow-right,
                        .btn-arrow-left, .btn-arrow-both {
                          position: relative;
                          padding-left: 18px;
                          padding-right: 18px;
                          border-radius: 0 !important;
                          margin-right: 1px; }
                          .btn-arrow-right[disabled],
                          .btn-arrow-left[disabled] {
                            opacity: 1.00; }

                          .btn-arrow-both:before, .btn-arrow-both:after,
                          .btn-arrow-right:before, .btn-arrow-right:after,
                          .btn-arrow-left:before,
                          .btn-arrow-left:after {
                            content: "";
                            position: absolute;
                            top: 4px;
                            /* move it down because of rounded corners */
                            height: 24px;
                            /* button_inner_height / sqrt(2) */
                            width: 24px;
                            /* same as height */
                            background: inherit;
                            /* use parent background */
                            border: inherit;
                            /* use parent border */
                            border-left-color: transparent;
                            /* hide left border */
                            border-bottom-color: transparent;
                            /* hide bottom border */
                            border-radius: 0 !important; }

                          .btn-arrow-both:before,
                          .btn-arrow-right:before,
                          .btn-arrow-left:before {
                            left: -13px; }

                          .btn-arrow-both:after,
                          .btn-arrow-right:after,
                          .btn-arrow-left:after {
                            right: -13px; }

                          .btn-arrow-right.btn-arrow-left,
                          .btn-arrow-left.btn-arrow-left {
                            padding-right: 36px; }

                            .btn-arrow-both:before,
                            .btn-arrow-right.btn-arrow-left:before, .btn-arrow-right.btn-arrow-left:after,
                            .btn-arrow-left.btn-arrow-left:before,
                            .btn-arrow-left.btn-arrow-left:after {
                              -webkit-transform: rotate(225deg);
                              -ms-transform: rotate(225deg);
                              transform: rotate(225deg);
                              /* rotate right arrow squares 45 deg to point right */ }

                          .btn-arrow-right.btn-arrow-right,
                          .btn-arrow-left.btn-arrow-right {
                            padding-left: 36px; }

                            .btn-arrow-both:after,
                            .btn-arrow-right.btn-arrow-right:before, .btn-arrow-right.btn-arrow-right:after,
                            .btn-arrow-left.btn-arrow-right:before,
                            .btn-arrow-left.btn-arrow-right:after {
                              -webkit-transform: rotate(45deg);
                              -ms-transform: rotate(45deg);
                              transform: rotate(45deg);
                              /* rotate right arrow squares 45 deg to point right */ }
                        }

                        /* Small */
                        .btn-sm.btn-arrow-right,
                        .btn-sm.btn-arrow-left,
                        .btn-sm.btn-arrow-both,
                        .btn-group-sm > .btn-arrow-left,
                        .btn-group-sm > .btn-arrow-right,
                        .btn-group-sm > .btn-arrow-both{
                          padding-left: 14px;
                          padding-right: 14px;
                          margin-right: -1px; }
                          .btn-sm.btn-arrow-right:before, .btn-sm.btn-arrow-right:after,
                          .btn-sm.btn-arrow-left:before,
                          .btn-sm.btn-arrow-left:after,
                          .btn-sm.btn-arrow-both:before,
                          .btn-sm.btn-arrow-both:after,
                          .btn-group-sm > .btn-arrow-left:before,
                          .btn-group-sm > .btn-arrow-left:after,
                          .btn-group-sm > .btn-arrow-right:before,
                          .btn-group-sm > .btn-arrow-right:after {
                            top: 4px;
                            /* move it down because of rounded corners */
                            height: 20px;
                            /* button_inner_height / sqrt(2) */
                            width: 20px;
                            /* same as height */ }
                          .btn-sm.btn-arrow-both:before,
                          .btn-sm.btn-arrow-right:before,
                          .btn-sm.btn-arrow-left:before,
                          .btn-group-sm > .btn-arrow-left:before,
                          .btn-group-sm > .btn-arrow-right:before {
                            left: -10px; }
                          .btn-sm.btn-arrow-both:after,
                          .btn-sm.btn-arrow-right:after,
                          .btn-sm.btn-arrow-left:after,
                          .btn-group-sm > .btn-arrow-left:after,
                          .btn-group-sm > .btn-arrow-right:after {
                            right: -10px; }
                          .btn-sm.btn-arrow-right.btn-arrow-left,
                          .btn-sm.btn-arrow-left.btn-arrow-left,
                          .btn-group-sm > .btn-arrow-left.btn-arrow-left,
                          .btn-group-sm > .btn-arrow-right.btn-arrow-left {
                            padding-right: 28px; }
                          .btn-sm.btn-arrow-right.btn-arrow-right,
                          .btn-sm.btn-arrow-left.btn-arrow-right,
                          .btn-group-sm > .btn-arrow-left.btn-arrow-right,
                          .btn-group-sm > .btn-arrow-right.btn-arrow-right {
                            padding-left: 28px; }
                        }

                        .btn-arrow-right:before,
                        .btn-arrow-left:after {
                          /* bring arrow pointers to front */
                          z-index: -3; }

                        .btn-arrow-right:after,
                        .btn-arrow-left:before {
                          /* bring arrow pointers to front */
                          z-index: 3; }

                        .btn-arrow-both:after, .btn-arrow-both:before {
                          z-index: 3;
                        }



                        .btn-arrow-right:before,
                        .btn-arrow-left:after {
                          /* hide arrow tails background */
                          background-color: white; }
</style>
<!-- HIT START -->
<div id="hit"><!-- ACCORDION START -->
<div class="container">
<div class="col-12 accordion" id="hitinfo"><!-- INSTRUCTIONS START -->
<div class="card">
<div class="card-header" id="instructionsHeading">
<h5 class="mb-0"><button aria-controls="instructions" aria-expanded="true" class="btn btn-link" data-target="#instructions" data-toggle="collapse" type="button">Instructions (click to expand/collapse)</button></h5>
</div>

<div aria-labelledby="instructionsHeading" class="collapse show" data-parent="#hitinfo" id="instructions">
<div class="card-body">
<p>Thanks for participating in this HIT! Please read the following instructions <em>carefully</em>.</p>

<div class="border bg-white pl-2 pt-2 border-success mb-3">
<p>SUMMARY:</p>

<p>In this HIT, you will be given a <span class="premise key-term">premise</span>, a <span class="hypothesis key-term">hypothesis</span>, and a <span class="key-term">context</span>. The <span class="key-term">context</span> can either <span class="strengthener key-term2">strengthen</span> or <span class="weakener key-term2">weaken</span> the hypothesis. You are also given <u>two</u> <span class="rationale key-term">rationales</span> that may explain or give hints about why the <span class="key-term">context</span> is <span class="strengthener key-term2">strengthener</span> or <span class="weakener key-term2">weakener</span>.</p>

<p>You will be asked to evaluate the quality of the rationales with respect to grammaticality, relevance, factual correctness, and whether they may explain why the context weakens or strengthens the hypothesis or not.</p>

<p>&nbsp;</p>
</div>
<!--
                                    <p>In this HIT, you will be given a <span class="premise key-term">premise</span>, a <span class="hypothesis key-term">hypothesis</span>, and a <span class=" key-term">context</span>. The <span class=" key-term">context</span> can either <span class="strengthener key-term2">strengthen</span> or
                                    <span class="weakener key-term2">weaken</span> the hypothesis. You are also given twelve <span class="rationale key-term">rationales</span> that may explain or give hints about why the <span class=" key-term">context</span> is <span class="strengthener key-term2">strengthener</span> or
                                    <span class="weakener key-term2">weakener</span>.</p>-->

<p>For each set of (<span class="premise">premise</span>, <span class="strengthener">strengthener</span>, <span class="hypothesis">hypothesis</span>) or (<span class="premise">premise</span>, <span class="weakener">weakener</span>, <span class="hypothesis">hypothesis</span>), you will be asked to <span class="key-term2">evaluate</span> the quality of <u>one</u> <span class="rationale key-term">rationales</span> on the following aspects:</p>

<ol>
	<li><font color="purple">Whether the rationale is grammatical, ungrammatical but understandable, or completely gibberish</font>. We are aware that some of the rationales are not fully grammatical. If you can still understand what the rationale says, even if it's an incomplete sentence or slightly ungrammatical, please select the "ungrammatical but understandable" option and you will proceed to evaluate the rationale on other aspects.</li>
	<li><font color="purple">Whether the rationale is relevant and on topic with respect to the premise, hypothesis and the context.</font> You should check this box if the rationale seems to directly talk about concepts in the premise, hypothesis or the context. Don't check the box if the rationale completely deviated from the topic.</li>
	<li><font color="purple">Factually correct or likely true</font>: Check this box if the rationale seems correct to you, or likely to be correct given the information you have.</li>
	<li><font color="purple">Provides a good explanation.</font> Check this box if the rationale explains or clarifies why the <span class="hypothesis">hypothesis</span> is <strong>more likely</strong> given the <span class="strengthener">strengthener</span> and <strong>less likely</strong> given the <span class="weakener">weakener</span>.</li>
</ol>

<p>Remember:</p>

<ul class="offset-1 col-10">
	<li class="mb-2">The <span class="premise key-term">premise</span> sentence describes <strong>a real-world situation</strong> and is always <em>assumed to be true</em>.</li>
	<li class="mt-2 mb-2">The <span class="hypothesis key-term">hypothesis</span> sentence describes <strong>an assumption or inference</strong> that we might make about that situation having read the <span class="premise">premise</span>. In most cases, the <span class="hypothesis">hypothesis</span> statement is <em>very likely</em> to be true given the <span class="premise">premise</span>; however, it is not necessarily <em>guaranteed</em> to be true.</li>
	<li class="mt-2 mb-2">A <span class="weakener key-term">weakener</span> is a statement that <span class="weakener">weakens</span> the <span class="hypothesis">hypothesis</span>;<br>
	it makes us much <strong>less likely</strong> to believe the <span class="hypothesis">hypothesis</span> is true.</li>
	<li class="mt-2">A <span class="strengthener   key-term">strengthener</span> is a statement that <span class="strengthener">strengthens</span> the <span class="hypothesis">hypothesis</span>;<br>
	it makes us much <strong>more likely</strong> to believe the <span class="hypothesis">hypothesis</span> is true.</li>
	<li class="mt-2">A <span class="rationale   key-term">rationale</span> is a statement that explains why the <span class="hypothesis">hypothesis</span> is <strong>more likely</strong> given the <span class="strengthener">strengthener</span> and <strong>less likely</strong> given the <span class="weakener">weakener</span>.</li>
</ul>
</div>
</div>
</div>

<div class="card">
<div class="card-header" id="exampleHeading">
<h5 class="mb-0"><button aria-controls="examples" aria-expanded="true" class="btn btn-link" data-target="#examples" data-toggle="collapse" type="button">Examples (click to expand/collapse)</button></h5>
</div>

<div aria-labelledby="exampleheading" class="collapse" data-parent="#hitinfo" id="examples">
<div class="card-body">
<div class="row">
<div class="col col-6"><positive-example> <span class="border">Good Example 1:</span><br>
<br>
<strong>Premise:</strong> <i>A baby boy in an elmo chair with lots of toys in the background.</i><br>
<strong>Hypothesis:</strong> <i>The baby boy in the elmo chair is happy.</i><br>
<br>
<strong>Weakener:</strong> <i>The baby boy's mom is wiping tears from his eyes.</i><br>
<br>
<br>
&nbsp;
<ol>
	<li><strong>Relevant rationale:</strong> <i>As a result, mom feels sad.</i></li>
	<li><strong>Factually correct rationale:</strong> the previous rationale, and also: "<i>The baby cried.</i>"</li>
	<li><strong>Provides a good explanation: </strong> All previous rationales, and also: "<i>The mom is wiping tears implies that the baby cries. The baby cannot cry and be happy at the same time.</i>"</li>
	<li><strong>Grammatical rationale:</strong> <i>The baby boy wanted to enjoy the moment</i></li>
	<li><strong>Ungrammatical but understandable rationale:</strong> <i>As a result, boy's mom feels to console.</i></li>
</ol>
<span class="border">Good Example 2:</span><br>
<br>
<strong>Premise:</strong> <i>A person wearing red and white climbs a foggy mountain.</i><br>
<strong>Hypothesis:</strong> <i>A person is rock climbing.</i><br>
<br>
<strong>Strengthener:</strong> <i>The person is attached to a rope going up the side of the mountain.</i><br>
<br>
<br>
&nbsp;
<ol>
	<li><strong>Relevant rationale:</strong> <i>Before, a person needed to get a rope.</i></li>
	<li><strong>Factually correct rationale:</strong> the previous rationales, and also: "<i>The person is a rock climber.</i>"</li>
	<li><strong>Provides a good explanation:</strong> All previous rationales, and also: "<i>The relationship between \"rope\" and \"climbing\" is that rope can be used for climbing.</i>"</li>
	<li><strong>Grammatical rationale:</strong> <i>The purpose of \"going up\" is to get a better view.</i></li>
	<li><strong>Ungrammatical but understandable rationale:</strong> <i>The definition of \"mountain\" is defined as highest point in the world.</i></li>
</ol>
</positive-example></div>

<div class="col col-6"><negative-example> <span class="border">Bad Example:</span><br>
<br>
<strong>Premise:</strong> <i>A baby boy in an elmo chair with lots of toys in the background.</i><br>
<strong>Hypothesis:</strong> <i>The baby boy in the elmo chair is happy.</i><br>
<br>
<strong>Weakener:</strong> <i>The baby boy's mom is wiping tears from his eyes.</i><br>
<br>
<br>
&nbsp;
<ol>
	<li><strong>Gibberish:</strong><i>The boy's eyes is then</i></li>
	<li><strong>Not relevant:</strong><i> Before, a person needed to go to a store.</i></li>
	<li><strong>Incorrect:</strong><i>The definition of \"chair\" is defined as same as desk.</i></li>
	<li><strong>Bad explanation: </strong> previous rationales, and also: "<i>The boy is sad because he is not playing with the toys.</i>" or "<i>The relationship between \"baby boy\" and \"happy\" is that of father.</i>"</li>
</ol>
</negative-example></div>
</div>
</div>
</div>
</div>
</div>
</div>
<!-- MTURK INPUT START -->

<div class="container pb-4 pt-3" id="mturk_form_container">
<input id="assignmentId" name="assignmentId" type="hidden" value=""> <input id="ee" name="ee" type="hidden">
<div class="offset-1">
<div class="sticky-top" id="instance_div" style="background-color: white">
<h4 class="premise key-term3" id="premise" name="premise"><strong>Premise:</strong> <i>A couple of newlyweds kissing underneath the bride's veil.</i></h4>

<h4 class="hypothesis key-term3" id="hypo" name="hypo"><strong>Hypothesis:</strong> <i>The newlyweds are kissing in a church during the wedding.</i></h4>

<h5 class="weakener key-term2" id="weakener" name="weakener"><strong>Weakener:</strong> <i>A casket is seen in the background.</i></h5>
</div>

<div id="weakener_rationales">
<div id="weakener_rationale1" name="weakener_rationale1"><!--<input type='hidden' id="weakener_rationale1_method" name="weakener_rationale1_method">rationale_bart-large /><br>--><input id="weakener_rationale1_method" name="weakener_rationale1_method" type="hidden" value="rationale_bart-large" style="">
<h6><strong>Rationale 1:</strong> <i>A couple of newlyweds kissing underneath the bride's veil implies that they are kissing in a church during the wedding</i></h6>

<table border="0" cellpadding="5" cellspacing="0" style="font-family: Verdana, Geneva, sans-serif; font-size:1em;">
	<tbody>
		<tr>
			<td>
			<div><input id="weakener_rationale1_gibberish" name="weakener_rationale1_gibberish_understandable_grammatical" onclick="toggle_gibberish('weakener_rationale1')" type="radio" value="gibberish"> <label for="gibberish">The rationale is completely gibberish, I can't understand it at all.</label><br>
			<input id="weakener_rationale1_understandable" name="weakener_rationale1_gibberish_understandable_grammatical" onclick="toggle_gibberish('weakener_rationale1')" type="radio" value="understandable"> <label for="understandable">The rationale is not perfectly grammatical, but I can understand it.</label><br>
			<input id="weakener_rationale1_grammatical" name="weakener_rationale1_gibberish_understandable_grammatical" onclick="toggle_gibberish('weakener_rationale1')" type="radio" value="grammatical" checked=""> <label for="grammatical">The rationale is grammatical.</label></div>
			</td>
		</tr>
		<tr>
			<td><input id="weakener_rationale1_relevant" name="weakener_rationale1_relevant" type="checkbox" checked=""> The rationale is on topic with respect to the premise and hypothesis.</td>
		</tr>
		<tr>
			<td><input id="weakener_rationale1_correct" name="weakener_rationale1_correct" type="checkbox"> The rationale is factually correct or likely true.</td>
		</tr>
		<tr>
			<td><input id="weakener_rationale1_explains" name="weakener_rationale1_explains" type="checkbox"> The rationale may explain why the rationale weakens the hypothesis.</td>
		</tr>
	</tbody>
</table>
</div>


&nbsp;

<div class="sticky-top" id="instance_div" style="background-color: white">
<h4 class="premise key-term3" id="premise" name="premise"><strong>Premise:</strong> <i>A couple of newlyweds kissing underneath the bride's veil.</i></h4>

<h4 class="hypothesis key-term3" id="hypo" name="hypo"><strong>Hypothesis:</strong> <i>The newlyweds are kissing in a church during the wedding.</i></h4>

<h5 class="strengthener key-term2" id="strengthener" name="strengthener"><strong>Strengthener:</strong> <i>A large cross is behind the couple.</i></h5>
</div>

<div id="strengthener_rationales">
<div id="strengthener_rationale1" name="strengthener_rationale1"><!--<hidden id="strengthener_rationale1_method" name="strengthener_rationale1_method">rationale_bart-large</hidden><br>--><input id="strengthener_rationale1_method" name="strengthener_rationale1_method" type="hidden" value="rationale_bart-large" style="">
<h6><strong>Rationale 1:</strong> <i>The couple cannot be kissing underneath the bride's veil if they are kissing in a church during the wedding</i></h6>

<table border="0" cellpadding="5" cellspacing="0" style="font-family: Verdana, Geneva, sans-serif; font-size:1em;">
	<tbody>
		<tr>
			<td>
			<div><input id="strengthener_rationale1_gibberish" name="strengthener_rationale1_gibberish_understandable_grammatical" onclick="toggle_gibberish('strengthener_rationale1')" type="radio" value="gibberish"> <label for="gibberish">The rationale is completely gibberish, I can't understand it at all.</label><br>
			<input id="strengthener_rationale1_understandable" name="strengthener_rationale1_gibberish_understandable_grammatical" onclick="toggle_gibberish('strengthener_rationale1')" type="radio" value="understandable"> <label for="understandable">The rationale is not perfectly grammatical, but I can understand it.</label><br>
			<input id="strengthener_rationale1_grammatical" name="strengthener_rationale1_gibberish_understandable_grammatical" onclick="toggle_gibberish('strengthener_rationale1')" type="radio" value="grammatical"> <label for="grammatical">The rationale is grammatical.</label></div>
			</td>
		</tr>
		<tr>
			<td><input disabled="true" id="strengthener_rationale1_relevant" name="strengthener_rationale1_relevant" type="checkbox"> The rationale is on topic with respect to the premise and hypothesis.</td>
		</tr>
		<tr>
			<td><input disabled="true" id="strengthener_rationale1_correct" name="strengthener_rationale1_correct" type="checkbox"> The rationale is factually correct or likely true.</td>
		</tr>
		<tr>
			<td><input disabled="true" id="strengthener_rationale1_explains" name="strengthener_rationale1_explains" type="checkbox"> The rationale may explain why the rationale strengthens the hypothesis.</td>
		</tr>
	</tbody>
</table>
</div>


</div>
<!-- OPTIONAL FEEDBACK -->

<div class="row mt-5">
<div class="col-8 offset-2 col-lg-6 offset-lg-3">
<p>(Optional) Please let us know if anything was unclear, if you experienced any issues, or if you have any other feedback for us.</p>
<textarea id="feedback" name="feedback" rows="3"></textarea></div>
</div>
<input name="time_spent" type="hidden" value="-1"> <!-- SUBMIT BUTTON -->
<div class="row mt-5">
<div class="col-2 offset-5"><input id="submitButton" onclick="getnext()" type="submit" value="Submit"></div>
</div>
</div>
<script language="Javascript">turkSetAssignmentID();</script></div>

<!-- MTURK INPUT END --></div>
<!-- HIT END --><!-- BOOSTRAP JS --><script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script><script>

                    // update debug display
                    // setInterval(function () {
                    //     document.getElementById('timing-debug').innerText = TimeMe.getTimeOnCurrentPageInSeconds();
                    // }, 0.1);
                </script><!-- HITPUB JS --><script id="hitpub_js">
                    (function () { var e, t; e = this, t = function () { var r = { startStopTimes: {}, idleTimeoutMs: 3e4, currentIdleTimeMs: 0, checkStateRateMs: 250, active: !1, idle: !1, currentPageName: "default-page-name", timeElapsedCallbacks: [], userLeftCallbacks: [], userReturnCallbacks: [], trackTimeOnElement: function (e) { var t = document.getElementById(e); t && (t.addEventListener("mouseover", function () { r.startTimer(e) }), t.addEventListener("mousemove", function () { r.startTimer(e) }), t.addEventListener("mouseleave", function () { r.stopTimer(e) }), t.addEventListener("keypress", function () { r.startTimer(e) }), t.addEventListener("focus", function () { r.startTimer(e) })) }, getTimeOnElementInSeconds: function (e) { var t = r.getTimeOnPageInSeconds(e); return t || 0 }, startTimer: function (e, t) { if (e || (e = r.currentPageName), void 0 === r.startStopTimes[e]) r.startStopTimes[e] = []; else { var n = r.startStopTimes[e], i = n[n.length - 1]; if (void 0 !== i && void 0 === i.stopTime) return } r.startStopTimes[e].push({ startTime: t || new Date, stopTime: void 0 }), r.active = !0, r.idle = !1 }, stopAllTimers: function () { for (var e = Object.keys(r.startStopTimes), t = 0; t < e.length; t++)r.stopTimer(e[t]) }, stopTimer: function (e, t) { e || (e = r.currentPageName); var n = r.startStopTimes[e]; void 0 !== n && 0 !== n.length && (void 0 === n[n.length - 1].stopTime && (n[n.length - 1].stopTime = t || new Date), r.active = !1) }, getTimeOnCurrentPageInSeconds: function () { return r.getTimeOnPageInSeconds(r.currentPageName) }, getTimeOnPageInSeconds: function (e) { var t = r.getTimeOnPageInMilliseconds(e); return void 0 === t ? void 0 : t / 1e3 }, getTimeOnCurrentPageInMilliseconds: function () { return r.getTimeOnPageInMilliseconds(r.currentPageName) }, getTimeOnPageInMilliseconds: function (e) { var t = r.startStopTimes[e]; if (void 0 !== t) { for (var n = 0, i = 0; i < t.length; i++) { var s = t[i].startTime, o = t[i].stopTime; void 0 === o && (o = new Date), n += o - s } return Number(n) } }, getTimeOnAllPagesInSeconds: function () { for (var e = [], t = Object.keys(r.startStopTimes), n = 0; n < t.length; n++) { var i = t[n], s = r.getTimeOnPageInSeconds(i); e.push({ pageName: i, timeOnPage: s }) } return e }, setIdleDurationInSeconds: function (e) { var t = parseFloat(e); if (!1 !== isNaN(t)) throw { name: "InvalidDurationException", message: "An invalid duration time (" + e + ") was provided." }; return r.idleTimeoutMs = 1e3 * e, this }, setCurrentPageName: function (e) { return r.currentPageName = e, this }, resetRecordedPageTime: function (e) { delete r.startStopTimes[e] }, resetAllRecordedPageTimes: function () { for (var e = Object.keys(r.startStopTimes), t = 0; t < e.length; t++)r.resetRecordedPageTime(e[t]) }, resetIdleCountdown: function () { r.idle && r.triggerUserHasReturned(), r.idle = !1, r.currentIdleTimeMs = 0 }, callWhenUserLeaves: function (e, t) { this.userLeftCallbacks.push({ callback: e, numberOfTimesToInvoke: t }) }, callWhenUserReturns: function (e, t) { this.userReturnCallbacks.push({ callback: e, numberOfTimesToInvoke: t }) }, triggerUserHasReturned: function () { if (!r.active) for (var e = 0; e < this.userReturnCallbacks.length; e++) { var t = this.userReturnCallbacks[e], n = t.numberOfTimesToInvoke; (isNaN(n) || void 0 === n || 0 < n) && (t.numberOfTimesToInvoke -= 1, t.callback()) } r.startTimer() }, triggerUserHasLeftPage: function () { if (r.active) for (var e = 0; e < this.userLeftCallbacks.length; e++) { var t = this.userLeftCallbacks[e], n = t.numberOfTimesToInvoke; (isNaN(n) || void 0 === n || 0 < n) && (t.numberOfTimesToInvoke -= 1, t.callback()) } r.stopAllTimers() }, callAfterTimeElapsedInSeconds: function (e, t) { r.timeElapsedCallbacks.push({ timeInSeconds: e, callback: t, pending: !0 }) }, checkState: function () { for (var e = 0; e < r.timeElapsedCallbacks.length; e++)r.timeElapsedCallbacks[e].pending && r.getTimeOnCurrentPageInSeconds() > r.timeElapsedCallbacks[e].timeInSeconds && (r.timeElapsedCallbacks[e].callback(), r.timeElapsedCallbacks[e].pending = !1); !1 === r.idle && r.currentIdleTimeMs > r.idleTimeoutMs ? (r.idle = !0, r.triggerUserHasLeftPage()) : r.currentIdleTimeMs += r.checkStateRateMs }, visibilityChangeEventName: void 0, hiddenPropName: void 0, listenForVisibilityEvents: function () { void 0 !== document.hidden ? (r.hiddenPropName = "hidden", r.visibilityChangeEventName = "visibilitychange") : void 0 !== document.mozHidden ? (r.hiddenPropName = "mozHidden", r.visibilityChangeEventName = "mozvisibilitychange") : void 0 !== document.msHidden ? (r.hiddenPropName = "msHidden", r.visibilityChangeEventName = "msvisibilitychange") : void 0 !== document.webkitHidden && (r.hiddenPropName = "webkitHidden", r.visibilityChangeEventName = "webkitvisibilitychange"), document.addEventListener(r.visibilityChangeEventName, function () { document[r.hiddenPropName] ? r.triggerUserHasLeftPage() : r.triggerUserHasReturned() }, !1), window.addEventListener("blur", function () { r.triggerUserHasLeftPage() }), window.addEventListener("focus", function () { r.triggerUserHasReturned() }), document.addEventListener("mousemove", function () { r.resetIdleCountdown() }), document.addEventListener("keyup", function () { r.resetIdleCountdown() }), document.addEventListener("touchstart", function () { r.resetIdleCountdown() }), window.addEventListener("scroll", function () { r.resetIdleCountdown() }), setInterval(function () { r.checkState() }, r.checkStateRateMs) }, websocket: void 0, websocketHost: void 0, setUpWebsocket: function (e) { if (window.WebSocket && e) { var t = e.websocketHost; try { r.websocket = new WebSocket(t), window.onbeforeunload = function () { r.sendCurrentTime(e.appId) }, r.websocket.onopen = function () { r.sendInitWsRequest(e.appId) }, r.websocket.onerror = function (e) { console && console.log("Error occurred in websocket connection: " + e) }, r.websocket.onmessage = function (e) { console && console.log(e.data) } } catch (e) { console && console.error("Failed to connect to websocket host.  Error:" + e) } } return this }, websocketSend: function (e) { r.websocket.send(JSON.stringify(e)) }, sendCurrentTime: function (e) { var t = { type: "INSERT_TIME", appId: e, timeOnPageMs: r.getTimeOnCurrentPageInMilliseconds(), pageName: r.currentPageName }; r.websocketSend(t) }, sendInitWsRequest: function (e) { var t = { type: "INIT", appId: e }; r.websocketSend(t) }, initialize: function (e) { var t = r.idleTimeoutMs || 30, n = r.currentPageName || "default-page-name", i = void 0, s = void 0; e && (t = e.idleTimeoutInSeconds || t, n = e.currentPageName || n, i = e.websocketOptions, s = e.initialStartTime), r.setIdleDurationInSeconds(t).setCurrentPageName(n).setUpWebsocket(i).listenForVisibilityEvents(), r.startTimer(void 0, s) } }; return r }, "undefined" != typeof module && module.exports ? module.exports = t() : "function" == typeof define && define.amd ? define([], function () { return e.TimeMe = t() }) : e.TimeMe = t() }).call(this);
                    TimeMe.initialize({
                        currentPageName: "task",
                        idleTimeoutInSeconds: 30
                    });

                    $(document).ready(function() {
                        $('#submitButton').click(function () {
                            try {
                                $('input[name=ee]').attr('value', TimeMe.getTimeOnCurrentPageInSeconds());
                            } catch {
                            }
                            return true;
                        });
                    });
                    $(document).ready(toggle_gibberish);

                    	function toggle_gibberish(curr_item) {
                            var gibberish = $("#" + curr_item + "_gibberish")[0];
                            is_gibberish = gibberish.checked !== undefined && gibberish.checked;

                            var relevant = $("#" + curr_item + "_relevant")[0];
                    		relevant.disabled = is_gibberish;
                    		relevant.checked = relevant.checked && !relevant.disabled;

                            var factual = $("#" + curr_item + "_correct")[0];
                            factual.disabled = is_gibberish;
                    		factual.checked = factual.checked && !factual.disabled;

                            var explains = $("#" + curr_item + "_explains")[0];
                            explains.disabled = is_gibberish;
                    		explains.checked = explains.checked && !explains.disabled;
                    	}


                </script></div></form>

      
    
  

</body></html>
""",
  os.path.join("img", "ex4.png"),
"self.actions.modify_checkbox('weakener_rationale1_relevant', 'on')"
  ]

  instance_5 = [
"""
Input name: coherence
HTML:
<html lang="en"><head>
    <title>Task</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
  </head>
  <body>
    <form name="mturk_form" method="post" id="mturk_form" target="_parent" action="#">

      <input type="hidden" name="csrfmiddlewaretoken" value="mxxOcvn5jEL7yVHlhiuinhjEiIAtwpy0kU5RiKRzY5fOqVTwgc2IiArDYf8KPFpp">
      

                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">


                    <!-- BOOTSTRAP CSS -->
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

                    <!-- HITPUB CSS -->
                    <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i,700,700i" rel="stylesheet">
                    <style id="hitpub_css">
                        /***********************************************
                        MOSAIC BOOSTRAP OVERWRITES
                        ***********************************************/
                        #hitinfo .card {
                            border-radius: 0;
                        }
                        #hitinfo .card:first-child {
                            border-bottom: 0;
                        }
                         #hitinfo button.btn-link {
                            color: #06486F;
                            text-decoration: none;
                         }
                        #hitinfo button.btn-link:hover {
                            text-decoration: none;
                        }
                        #hit ul.question-choice {
                            list-style-type: none;
                        }
                        /***********************************************
                        MOSAIC GENERAL STYLING
                        ***********************************************/
                         body {
                             font-family: "Open Sans", "Roboto", sans-serif;
                         }
                        textarea#feedback {
                            width: 100%
                        }
                        input#submitButton {
                            margin: auto;
                            display: block;
                            background-color: #2172a4;
                            color: #fff;
                            font-size: 1.125rem;
                            padding: .5rem 1rem;
                            cursor: pointer;
                            border-radius: 1rem;
                        }
                        input#submitButton:hover {
                            background-color: #06486F;
                        }

                        .key-term1{
                            color: #0072B2;
                            font-weight:bold;
                        }

                        .key-term2{
                            color:#D55E00;
                            font-weight:bold;
                        }

                        .key-term3{
                            color: #CC79A7;
                            font-weight:bold;
                        }

                    </style>
                   <div id="hit" class="container">
                        <div class="col-8 offset-2">
                            <div class="accordion" id="hitinfo">
                                <!-- INSTRUCTIONS START -->
                                <div class="card">
                                    <div class="card-header" id="instructionsHeading">
                                        <h5 class="mb-0">
                                            <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#instructions" aria-expanded="true" aria-controls="instructions">
                                                Instructions (click to expand)
                                            </button>
                                        </h5>
                                    </div>
                                    <div class="collapse" id="instructions" aria-labelledby="instructionsHeading" data-parent="#hitinfo">
                                        <div class="card-body">
                                            <p> In this HIT you will be presented with a <span class="key-term1">excerpt from a Wikipedia article</span> that acts as a prompt and a
                                            <span class="key-term2">system's automatically-generated continuation</span> of that excerpt.
                                            Your job is to rate the quality of the <span class="key-term2">system generation</span> across three axes:</p>
                                            <ul>
                                            <li> <strong>Coherence:</strong> <em> Is the system's generation <u>aligned in meaning and topic with the prompt?</u></em></li>
                                            <li> <strong>Fluency:</strong> <em> Is the system's generation <u>grammatical, easy-to-read, and not repetitive?</u></em> </li>
                                            <li> <strong>Overall:</strong> <em> All things considered, how good is the system's completion?</em></li>
                                            </ul>

                                            <p>You will be able to rate each of the three axes on a scale from 1 to 5, with
                                            <span style="color:red;">1 being the lowest/worst</span> and
                                            <span style="color:green;">5 the highest/best</span>. The specific scales are:</p>
                                            <ul>
                                                <li> <strong>Coherence:</strong>
                                                    <ul>
                                                        <li> <strong style="color:green;">5/5 (excellent):</strong> The system's result is perfectly in line with the prompt; topically speaking, I could see
                                                        this type of continuation appearing in a Wikipedia article. </li>
                                                        <li> 4/5: The system's result is closely related to the prompt with some minor errors that do not affect overall relevance to the prompt.</li>
                                                        <li> 3/5: The system's result is, to some extent, relevant to the prompt, but there are some errors/irrelevant parts that stray from what a human might write.</li>
                                                        <li> 2/5: At the first glance, the system's result seems somewhat related to the prompt, but the semantic inconsistency can be easily spotted.</li>
                                                        <li> <strong style="color:red;">1/5 (bad):</strong> The system's result is completely off topic, or is semantically contradictory to the content contained in the prompt.</li>
                                                    </ul>
                                                </li>

                                                <li> <strong>Fluency:</strong>
                                                    <ul>
                                                    <li> <strong style="color:green;">5/5 (excellent):</strong> The system's result is human-like, grammatically correct, not repetitive, introduces new content beyond the prompt, and is very easy to understand.</li>
                                                    <li> 4/5: Very good fluency, but I could probably tell a machine wrote it based on a minor grammar error, an awkward reptition of the prompt, or other small mistake.</li>
                                                    <li> 3/5: The system's result definitely contains minor errors, unnatural repetition, or awkward sentence-by-sentence progression, but I'm able to mostly understand.</li>
                                                    <li> 2/5: While I managed to read most of the continuation, the grammar/language errors are difficult to overlook, there are many unnatural repetitions, or the continuation doesn't go beyond the prompt at all.</li>
                                                    <li> <strong style="color:red;">1/5 (bad):</strong> The system's result does not make sense and it is unreadable.</li>
                                                    </ul>
                                                </li>

                                                <li> <strong>Overall:</strong>
                                                    <ul>
                                                    <li> <strong style="color:green;">5/5 (excellent):</strong> The system's result is very informative, contains novel content, and seems plausible. It displays the right level of diversity and is enjoyable to read.</li>
                                                    <li> 4/5: Pretty good.</li>
                                                    <li> 3/5: Just okay.</li>
                                                    <li> 2/5: Mediocre.</li>
                                                    <li> <strong style="color:red;">1/5 (bad):</strong> The system's result is dull, repetitive, difficult to read.
                                                    It doesn't contribute anything new, or, what it does contriubte is obviously wrong/nonsensical.</li>
                                                    </ul>
                                                </li>
                                            </ul>
                                            <br>
                                            <em>Note: While you should incorporate correctness into your "Overall" rating (e.g., if the system says "Superman won the World Cup", you should deduct points),
                                            it's okay to rely on what you know and only deduct for obviously wrong information.
                                            There's no need to search on your own to verify the correctness of the presented facts. </em>
                                        </div>

                                    </div>
                                </div>
                                <!-- INSTRUCTIONS END -->

                                <!-- EXAMPLES START -->
                                <div class="card">
                                    <div class="card-header" id="examplesHeading">
                                        <h5 class="mb-0">
                                            <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#examples" aria-expanded="true" aria-controls="examples">
                                                Examples (click to expand)
                                            </button>
                                        </h5>
                                    </div>
                                    <div class="collapse" id="examples" aria-labelledby="examplesHeading" data-parent="#hitinfo">
                                        <div class="card-body">

                                            <h3>Example 1 (bad completion):</h3>

                                            <div class="row">
                                                <div class="col-12">
                                                    <h5><span class="key-term1">Prompt:</span></h5>
                                                    <div class="col-12 align-text-center">
                                                        <fieldset style="border: 1px solid #0072B2; margin: 20px; padding: 0 10px 10px; border-radius: 8px; padding-top: 10px; box-shadow: 0 0 3px #666;">
                                                            ... Animals in the Trout Creek Mountains are adapted to the environment of the High Desert. Pronghorn are common in the open, sagebrush-covered...
                                                        </fieldset>
                                                    </div>
                                                </div>
                                            </div>

                                            <div class="row">
                                                <div class="col-12">
                                                    <h5><span class="key-term2">System's generation <u>(rate this!)</u>:</span></h5>
                                                    <div class="col-12 align-text-center">
                                                        <fieldset style="border: 1px solid #D55E00; margin: 20px; padding: 0 10px 10px; border-radius: 8px; padding-top: 10px; box-shadow: 0 0 3px #666;">
                                                            ... watershed, where sea lions have become widespread due to habitat loss, and have been the dominant species since the Conquest of the Rocky Mountains.
                                                            Altogether these animals are often found alone, detached from their surroundings, feeding on other animals, lice, and other similar items.
                                                            After the commercial logging and expansion of the Rogue River and the construction of the Burnett Basin,
                                                            the Elk River valley became a common center of pastoral activity. Elk River residents have settled...
                                                        </fieldset>
                                                    </div>
                                                </div>
                                            </div>
                                            <br>
                                            <ul>
                                                <li> <strong style="color:lightcoral">Coherence: 2/5</strong> <em>Why?</em> The completion is partly related to animals, but
                                                    the prompt is about the animals in the mountains, while the completion talks about a watershed with sea lions (and then talks about Elk River residents and flowers). </li>
                                                <li> <strong>Fluency: 3/5</strong> <em>Why?</em> The sentences are individually grammatically correct without repetition,
                                                but they are difficult to read because the topic changes very frequently. </li>
                                                <li> <strong style="color:lightcoral">Overall: 2/5</strong>  <em>Why?</em> Each sentence provides new information beyond the prompt,
                                                but there's a significant amount of obviously incorrect information (e.g., I know sea lions don't eat lice, and wouldn't be a dominant species in the Rocky Mountains).
                                                Furthermore, while this isn't a repetitive generation, it "jumps around" topically more than it should. </li>
                                            </ul>

                                            <em> Note: for the "Overall" rating, there are other incorrect pieces of information in the system's output
                                            (e.g., the Trout Creek Mountains are not in the Rocky Mountains). But only consider factual mistakes that are obvious to you
                                            without additional research --- there's no need to verify every new fact that the system generates. </em>

                                            <br>
                                            <br>
                                            <h3>Example 2 (good completion):</h3>

                                            <div class="row">
                                                <div class="col-12">
                                                    <h5><span class="key-term1">Prompt:</span></h5>
                                                    <div class="col-12 align-text-center">
                                                        <fieldset style="border: 1px solid #0072B2; margin: 20px; padding: 0 10px 10px; border-radius: 8px; padding-top: 10px; box-shadow: 0 0 3px #666;">
                                                            ... Richmond fell ill the day after the 1986 NASCAR annual banquet during a promotional trip to New York. He was not well enough to begin the 1987 NASCAR season despite...
                                                        </fieldset>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-12">
                                                    <h5><span class="key-term2">System's generation <u>(rate this!)</u>:</span></h5>
                                                    <div class="col-12 align-text-center">
                                                        <fieldset style="border: 1px solid #D55E00; margin: 20px; padding: 0 10px 10px; border-radius: 8px; padding-top: 10px; box-shadow: 0 0 3px #666;">
                                                            ... lengthy hospitalization in Cleveland and further rest at home; when Richmond missed the Daytona 500, his condition was reported as double pneumonia.
                                                            Media later reported that he had tested positive for acquired immune deficiency syndrome (AIDS).
                                                            He returned to Pocono for the Miller High Life 500 during the middle of the year.
                                                            Starting third, he led by the fifth lap and ultimately led 82 laps, including the final 46,
                                                            to win the race by eight car-lengths over Bill Elliott. In the middle of the race, Richmond's car suffered gearbox problems...
                                                        </fieldset>
                                                    </div>
                                                </div>
                                            </div>
                                            <br>

                                            <ul>
                                                <li> <strong style="color:green">Coherence: 5/5</strong> <em>Why?</em>
                                                The completion is well-aligned with the prompt, because it continues to describe the health and career of a NASCAR driver. </li>

                                                <li> <strong style="color:green">Fluency: 5/5</strong> <em>Why?</em> The sentences are grammatically correct,
                                                and flow nicely as a career summary of the NASCAR driver.</li>

                                                <li> <strong style="color:green">Overall: 5/5</strong>  <em>Why?</em> The completion doesn't repeat information in the prompt, and also provides interesting new information
                                                about the driver's career that could definitely be correct.</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- MTURK INPUT START -->
                        <div class="col-8 mt-5 offset-2 align-content-center">
                            
                                <input type="hidden" value="" name="assignmentId" id="assignmentId">
                                <input type="hidden" name="ee" id="ee">

                                <div class="row">
                                    <div class="col-12">
                                        <h5><span class="key-term1">Prompt (do your best to understand the gist, even if it's hard!):</span></h5>
                                        <div class="col-12 align-text-center">
                                            <fieldset style="border: 1px solid #0072B2; margin: 20px; padding: 0 10px 10px; border-radius: 8px; padding-top: 10px; box-shadow: 0 0 3px #666;">
                                                Rebuilt after the war, the city entered a "Golden Age" it become the largest city in Mississippi between 1890 and 1930, and a leading center for manufacturing...
                                            </fieldset>
                                        </div>
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-12">
                                        <h5><span class="key-term2">System's generation <u>(rate this!)</u>:</span></h5>
                                        <div class="col-12 align-text-center">
                                        <fieldset style="border: 1px solid #D55E00; margin: 20px; padding: 0 10px 10px; border-radius: 8px; padding-top: 10px; box-shadow: 0 0 3px #666;">
                                            ...and trade. The city was also the site of the first major slave trade in the United States.
The city was also the site of the first major slave-owned plantation in the South, and the first major industrial city in the United Kingdom. The city was also the site of the "<unk>" in the name of the "<penny ",="" a="" term="" that="" was="" used="" to="" describe="" the"="" <="" hard="" or="" "hard-white="" cotton,="" and="" cotton-sugar.="" the="" also="" in="" name="" of="" a"="" <pry="" fieldset="">

                                        </penny></unk></fieldset></div>
                                    </div>
                                </div>

                                <div class="row align-content-center mt-5">
                                    <div class="col-12 align-content-center">
                                        <div class="form-group">
                                            <label for="coherence" id="coherencelabel" style="font-size: 32px"><strong>Coherence: 3/5</strong></label>
                                            <br>
                                            <small> <em> Is the system's generation <u>aligned in meaning and topic with the prompt?</u></em> </small>
                                            <br>
                                            <label class="float-left" style="color:red;">Bad</label>
                                            <label class="float-right" style="color:green;">Excellent</label>
                                            <br>
                                            <input type="range" class="form-control-range" id="coherence" name="coherence" min="1" max="5" step="1" value="4" list="coherence_list">
                                            <datalist id="coherence_list">
                                                <option value="1" label="bad">
                                                </option><option value="2" label="mediocre">
                                                </option><option value="3" label="okay">
                                                </option><option value="4" label="good">
                                                </option><option value="5" label="excellent">
                                            </option></datalist>
                                            <small id="coherenceHelp" class="form-text text-muted" style="min-height:70px;">
                                               The system's result is, to some extent, relevant to the prompt, but there are some errors/irrelevant parts that stray from what a human might write.
                                            </small>
                                        </div>
                                    </div>
                                </div>

                                <div class="row align-content-center">
                                    <div class="col-12 align-content-center">
                                        <div class="form-group">
                                            <label for="fluency" id="fluencylabel" style="font-size: 32px"><strong>Fluency: 3/5</strong></label>
                                            <br>
                                            <small> <em> Is the system's generation <u>grammatical, easy-to-read, and not repetitive? </u></em> </small>
                                            <br>
                                            <label class="float-left" style="color:red;">Bad</label>
                                            <label class="float-right" style="color:green;">Excellent</label>
                                            <br>
                                            <input type="range" class="form-control-range" id="fluency" name="fluency" min="1" max="5" step="1" value="3" list="fluency_list">
                                            <datalist id="fluency_list">
                                                <option value="1" label="bad">
                                                </option><option value="2" label="mediocre">
                                                </option><option value="3" label="okay">
                                                </option><option value="4" label="good">
                                                </option><option value="5" label="excellent">
                                            </option></datalist>
                                            <small id="fluencyHelp" class="form-text text-muted" style="min-height:70px;">
                                                The system's result definitely contains minor errors, unnatural repetition, or awkward sentence-by-sentence progression, but I'm able to mostly understand.
                                            </small>
                                        </div>
                                    </div>
                                </div>

                                <div class="row align-content-center">
                                    <div class="col-12 align-content-center">
                                        <div class="form-group">
                                            <label for="overall" id="overalllabel" style="font-size: 32px"><strong>Overall: 3/5</strong></label>
                                            <br>
                                            <small> <em> All things considered, <u>how good is the system's generation?</u> </em> </small>
                                            <br>
                                            <label class="float-left" style="color:red;">Bad</label>
                                            <label class="float-right" style="color:green;">Excellent</label>
                                            <br>
                                            <input type="range" class="form-control-range" id="overall" name="overall" min="1" max="5" step="1" value="3" list="overall_list">
                                            <datalist id="overall_list">
                                                <option value="1" label="bad">
                                                </option><option value="2" label="mediocre">
                                                </option><option value="3" label="okay">
                                                </option><option value="4" label="good">
                                                </option><option value="5" label="excellent">
                                            </option></datalist>
                                            <small id="overallHelp" class="form-text text-muted" style="min-height:70px;">
                                                Just okay.
                                            </small>
                                        </div>
                                    </div>
                                </div>

                                <!-- OPTIONAL FEEDBACK -->
                                <div class="row mt-5">
                                    <div class="col-8 offset-2 col-lg-6 offset-lg-3">
                                        <p>(Optional) Please let us know if anything was unclear, if you experienced any issues, or if you have any other feedback for us.</p>
                                        <textarea id="feedback" name="feedback" rows="3"></textarea>
                                    </div>
                                </div>

                                <!-- SUBMIT BUTTON -->
                                <div class="row mt-5">
                                    <div class="col-2 offset-5">
                                        <input id="submitButton" onclick="getnext()" type="submit" value="Submit">
                                    </div>
                                </div>

                            
                            <script language="Javascript">turkSetAssignmentID();</script>
                        </div>
                        <!-- MTURK INPUT END -->

                    </div></form>
		            <!-- HIT END -->

                    <!-- BOOSTRAP JS -->
                    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
                    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

                    <!-- HITPUB JS -->
                    <script id="hitpub_js">

                        // TimeMe.js
                        (function () { var e, t; e = this, t = function () { var r = { startStopTimes: {}, idleTimeoutMs: 3e4, currentIdleTimeMs: 0, checkStateRateMs: 250, active: !1, idle: !1, currentPageName: "default-page-name", timeElapsedCallbacks: [], userLeftCallbacks: [], userReturnCallbacks: [], trackTimeOnElement: function (e) { var t = document.getElementById(e); t && (t.addEventListener("mouseover", function () { r.startTimer(e) }), t.addEventListener("mousemove", function () { r.startTimer(e) }), t.addEventListener("mouseleave", function () { r.stopTimer(e) }), t.addEventListener("keypress", function () { r.startTimer(e) }), t.addEventListener("focus", function () { r.startTimer(e) })) }, getTimeOnElementInSeconds: function (e) { var t = r.getTimeOnPageInSeconds(e); return t || 0 }, startTimer: function (e, t) { if (e || (e = r.currentPageName), void 0 === r.startStopTimes[e]) r.startStopTimes[e] = []; else { var n = r.startStopTimes[e], i = n[n.length - 1]; if (void 0 !== i && void 0 === i.stopTime) return } r.startStopTimes[e].push({ startTime: t || new Date, stopTime: void 0 }), r.active = !0, r.idle = !1 }, stopAllTimers: function () { for (var e = Object.keys(r.startStopTimes), t = 0; t < e.length; t++)r.stopTimer(e[t]) }, stopTimer: function (e, t) { e || (e = r.currentPageName); var n = r.startStopTimes[e]; void 0 !== n && 0 !== n.length && (void 0 === n[n.length - 1].stopTime && (n[n.length - 1].stopTime = t || new Date), r.active = !1) }, getTimeOnCurrentPageInSeconds: function () { return r.getTimeOnPageInSeconds(r.currentPageName) }, getTimeOnPageInSeconds: function (e) { var t = r.getTimeOnPageInMilliseconds(e); return void 0 === t ? void 0 : t / 1e3 }, getTimeOnCurrentPageInMilliseconds: function () { return r.getTimeOnPageInMilliseconds(r.currentPageName) }, getTimeOnPageInMilliseconds: function (e) { var t = r.startStopTimes[e]; if (void 0 !== t) { for (var n = 0, i = 0; i < t.length; i++) { var s = t[i].startTime, o = t[i].stopTime; void 0 === o && (o = new Date), n += o - s } return Number(n) } }, getTimeOnAllPagesInSeconds: function () { for (var e = [], t = Object.keys(r.startStopTimes), n = 0; n < t.length; n++) { var i = t[n], s = r.getTimeOnPageInSeconds(i); e.push({ pageName: i, timeOnPage: s }) } return e }, setIdleDurationInSeconds: function (e) { var t = parseFloat(e); if (!1 !== isNaN(t)) throw { name: "InvalidDurationException", message: "An invalid duration time (" + e + ") was provided." }; return r.idleTimeoutMs = 1e3 * e, this }, setCurrentPageName: function (e) { return r.currentPageName = e, this }, resetRecordedPageTime: function (e) { delete r.startStopTimes[e] }, resetAllRecordedPageTimes: function () { for (var e = Object.keys(r.startStopTimes), t = 0; t < e.length; t++)r.resetRecordedPageTime(e[t]) }, resetIdleCountdown: function () { r.idle && r.triggerUserHasReturned(), r.idle = !1, r.currentIdleTimeMs = 0 }, callWhenUserLeaves: function (e, t) { this.userLeftCallbacks.push({ callback: e, numberOfTimesToInvoke: t }) }, callWhenUserReturns: function (e, t) { this.userReturnCallbacks.push({ callback: e, numberOfTimesToInvoke: t }) }, triggerUserHasReturned: function () { if (!r.active) for (var e = 0; e < this.userReturnCallbacks.length; e++) { var t = this.userReturnCallbacks[e], n = t.numberOfTimesToInvoke; (isNaN(n) || void 0 === n || 0 < n) && (t.numberOfTimesToInvoke -= 1, t.callback()) } r.startTimer() }, triggerUserHasLeftPage: function () { if (r.active) for (var e = 0; e < this.userLeftCallbacks.length; e++) { var t = this.userLeftCallbacks[e], n = t.numberOfTimesToInvoke; (isNaN(n) || void 0 === n || 0 < n) && (t.numberOfTimesToInvoke -= 1, t.callback()) } r.stopAllTimers() }, callAfterTimeElapsedInSeconds: function (e, t) { r.timeElapsedCallbacks.push({ timeInSeconds: e, callback: t, pending: !0 }) }, checkState: function () { for (var e = 0; e < r.timeElapsedCallbacks.length; e++)r.timeElapsedCallbacks[e].pending && r.getTimeOnCurrentPageInSeconds() > r.timeElapsedCallbacks[e].timeInSeconds && (r.timeElapsedCallbacks[e].callback(), r.timeElapsedCallbacks[e].pending = !1); !1 === r.idle && r.currentIdleTimeMs > r.idleTimeoutMs ? (r.idle = !0, r.triggerUserHasLeftPage()) : r.currentIdleTimeMs += r.checkStateRateMs }, visibilityChangeEventName: void 0, hiddenPropName: void 0, listenForVisibilityEvents: function () { void 0 !== document.hidden ? (r.hiddenPropName = "hidden", r.visibilityChangeEventName = "visibilitychange") : void 0 !== document.mozHidden ? (r.hiddenPropName = "mozHidden", r.visibilityChangeEventName = "mozvisibilitychange") : void 0 !== document.msHidden ? (r.hiddenPropName = "msHidden", r.visibilityChangeEventName = "msvisibilitychange") : void 0 !== document.webkitHidden && (r.hiddenPropName = "webkitHidden", r.visibilityChangeEventName = "webkitvisibilitychange"), document.addEventListener(r.visibilityChangeEventName, function () { document[r.hiddenPropName] ? r.triggerUserHasLeftPage() : r.triggerUserHasReturned() }, !1), window.addEventListener("blur", function () { r.triggerUserHasLeftPage() }), window.addEventListener("focus", function () { r.triggerUserHasReturned() }), document.addEventListener("mousemove", function () { r.resetIdleCountdown() }), document.addEventListener("keyup", function () { r.resetIdleCountdown() }), document.addEventListener("touchstart", function () { r.resetIdleCountdown() }), window.addEventListener("scroll", function () { r.resetIdleCountdown() }), setInterval(function () { r.checkState() }, r.checkStateRateMs) }, websocket: void 0, websocketHost: void 0, setUpWebsocket: function (e) { if (window.WebSocket && e) { var t = e.websocketHost; try { r.websocket = new WebSocket(t), window.onbeforeunload = function () { r.sendCurrentTime(e.appId) }, r.websocket.onopen = function () { r.sendInitWsRequest(e.appId) }, r.websocket.onerror = function (e) { console && console.log("Error occurred in websocket connection: " + e) }, r.websocket.onmessage = function (e) { console && console.log(e.data) } } catch (e) { console && console.error("Failed to connect to websocket host.  Error:" + e) } } return this }, websocketSend: function (e) { r.websocket.send(JSON.stringify(e)) }, sendCurrentTime: function (e) { var t = { type: "INSERT_TIME", appId: e, timeOnPageMs: r.getTimeOnCurrentPageInMilliseconds(), pageName: r.currentPageName }; r.websocketSend(t) }, sendInitWsRequest: function (e) { var t = { type: "INIT", appId: e }; r.websocketSend(t) }, initialize: function (e) { var t = r.idleTimeoutMs || 30, n = r.currentPageName || "default-page-name", i = void 0, s = void 0; e && (t = e.idleTimeoutInSeconds || t, n = e.currentPageName || n, i = e.websocketOptions, s = e.initialStartTime), r.setIdleDurationInSeconds(t).setCurrentPageName(n).setUpWebsocket(i).listenForVisibilityEvents(), r.startTimer(void 0, s) } }; return r }, "undefined" != typeof module && module.exports ? module.exports = t() : "function" == typeof define && define.amd ? define([], function () { return e.TimeMe = t() }) : e.TimeMe = t() }).call(this);

                        TimeMe.initialize({
                            currentPageName: "task",
                            idleTimeoutInSeconds: 30
                        });



                        $(document).ready(function() {
                            var cookie_name = '_task_repetition_v1';

                            $('.collapse').collapse({ 'toggle': false }).on('hidden.bs.collapse', function() {
                        	if (this.id) {
                                    localStorage[this.id + cookie_name] = 'true';
                        	}
                            }).on('shown.bs.collapse', function() {
                        	if (this.id) {
                                    localStorage.removeItem(this.id + cookie_name);
                        	}
                            }).each(function() {
                        	if (this.id && localStorage[this.id + cookie_name] == 'true' ) {
                                    $(this).collapse('hide');
                        	}
                            });


                            $('#submitButton').click(function () {
                                try {
                                    $('input[name=ee]').attr('value', TimeMe.getTimeOnCurrentPageInSeconds());
                                } catch {
                                }
                                return true;
                            });

                            $('#coherence').on('input', function() {
                                var value = $(this).val()
                                if(value == 5) {
                                    $('#coherenceHelp').text(
                                        "The system's result is perfectly in line with the prompt; topically speaking, I could see "+
                                        "this type of continuation appearing in a Wikipedia article.");
                                    $('#coherencelabel').html('<strong style="color:green;">Coherence: 5/5</strong>');
                                }
                                else if(value == 4) {
                                    $('#coherenceHelp').text("The system's result is closely related to the prompt with some minor errors that do not affect overall relevance to the prompt.");
                                    $('#coherencelabel').html('<strong style="color:mediumseagreen;">Coherence: 4/5</strong>');
                                }
                                else if(value == 3) {
                                    $('#coherenceHelp').text("The system's result is, to some extent, relevant to the prompt, but there are some errors/irrelevant parts that stray from what a human might write.");
                                    $('#coherencelabel').html('<strong>Coherence: 3/5</strong>');
                                }
                                else if(value == 2) {
                                    $('#coherenceHelp').text("At the first glance, the system's result seems somewhat related to the prompt, but the semantic inconsistency can be easily spotted.");
                                    $('#coherencelabel').html('<strong style="color:lightcoral">Coherence: 2/5</strong>');
                                }
                                else if(value == 1) {
                                    $('#coherenceHelp').text("The system's result is completely off topic, or is semantically contradictory to the content contained in the prompt.");
                                    $('#coherencelabel').html('<strong style="color:red">Coherence: 1/5</strong>');
                                }
                            });

                            $('#fluency').on('input', function() {
                                var value = $(this).val()
                                if(value == 5) {
                                    $('#fluencyHelp').text(
                                        "The system's result is human-like, grammatically correct, not repetitive, introduces new content beyond the prompt, and is very easy to understand.");
                                    $('#fluencylabel').html('<strong style="color:green;">Fluency: 5/5</strong>');
                                }
                                else if(value == 4) {
                                    $('#fluencyHelp').text("Very good fluency, but I could probably tell a machine wrote it based on a minor grammar error, an awkward reptition of the prompt, or other small mistake.");
                                    $('#fluencylabel').html('<strong style="color:mediumseagreen;">Fluency: 4/5</strong>');
                                }
                                else if(value == 3) {
                                    $('#fluencyHelp').text("The system's result definitely contains minor errors, unnatural repetition, or awkward sentence-by-sentence progression, but I'm able to mostly understand.");
                                    $('#fluencylabel').html('<strong>Fluency: 3/5</strong>');
                                }
                                else if(value == 2) {
                                    $('#fluencyHelp').text("While I managed to read most of the continuation, the grammar/language errors are difficult to overlook, there are many unnatural repetitions, or the continuation doesn't go beyond the prompt at all.");
                                    $('#fluencylabel').html('<strong style="color:lightcoral">Fluency: 2/5</strong>');
                                }
                                else if(value == 1) {
                                    $('#fluencyHelp').text("The system's result does not make sense and it is unreadable.");
                                    $('#fluencylabel').html('<strong style="color:red">Fluency: 1/5</strong>');
                                }
                            });

                            $('#overall').on('input', function() {
                                var value = $(this).val()
                                if(value == 5) {
                                    $('#overallHelp').text(
                                        "The system's result is very informative, contains novel content, and seems plausible. It displays the right level of diversity and is enjoyable to read.");
                                    $('#overalllabel').html('<strong style="color:green;">Overall: 5/5</strong>');
                                }
                                else if(value == 4) {
                                    $('#overallHelp').text("Pretty good");
                                    $('#overalllabel').html('<strong style="color:mediumseagreen;">Overall: 4/5</strong>');

                                }
                                else if(value == 3) {
                                    $('#overallHelp').text("Just okay.");
                                    $('#overalllabel').html('<strong>Overall: 3/5</strong>');
                                }
                                else if(value == 2) {
                                    $('#overallHelp').text("Mediocre.");
                                    $('#overalllabel').html('<strong style="color:lightcoral">Overall: 2/5</strong>');
                                }
                                else if(value == 1) {
                                    $('#overallHelp').text("The system's result is dull, repetitive, difficult to read. It doesn't contribute anything new, or, what it does contriubte is obviously wrong/nonsensical.");
                                    $('#overalllabel').html('<strong style="color:red">Overall: 1/5</strong>');
                                }
                            });




                        });

                    </script>

      
    
  

</body></html>
""",
  os.path.join("img", "ex5.png"),
"self.actions.modify_range('coherence', '4.0')"
  ]

  instance_6 = [
"""
Input name: story1
HTML:
<html><head>
    <title>Task</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
  </head>
  <body>
    <form name="mturk_form" method="post" id="mturk_form" target="_parent" action="#">

      <input type="hidden" name="csrfmiddlewaretoken" value="rUGHX3U1TSal865u22c3mgWha8mHFTp3syaPiG5aGeHeTjyKIeGMqXnnBi6uZ6z1">
      <style type="text/css">body {
													font-family: 'Helvetica', 'Arial', sans-serif;
													color: #444444;
													font-size: 12pt;
													background-color: #FAFAFA;
												}

												mark {
													background-color: rgb(153,50,204,0.3);
													color: black;
												}

												ul {
													text-align: left;
													list-style-position: inside;
												}

												textarea {
												font-size: 18px;
												margin: 0 auto;
												display: block;
												}

												#submitButton {
													font-size:20pt;
													color:white;
													background-color:green;
													border:2px solid #336600;
													padding:3px;
												}

											   table {
												   border-spacing: 5;
											   }

											   .bb {
												   border-bottom: 2px dotted black;
											   }
</style>
<h1 align="center"><span style="color:#B22222;">New Pilot Study:</span> Writing fluent yet&nbsp;<strong>inconsistent</strong> stories</h1>

<h3 align="center"><mark>Overview</mark></h3>

<div style="width:1000px; margin:0 auto;">You will be shown an incomplete three-part story. Write the missing part so that it preserves the <strong>narrative flow</strong> but introduces a logical <strong>inconsistency</strong>.</div>

<h3 align="center"><mark>Instructions</mark></h3>

<div style="width:1000px; margin:0 auto;">
<ol>
	<li>Review an incomplete three-part story. The beginning and the ending of the story are given.</li>
	<li>Write&nbsp;the&nbsp;middle of the story that flows nicely from the beginning to the ending, but makes the whole story <em>very unlikely</em>, <em>improbable</em>, or <em>inconsistent</em>.</li>
</ol>
</div>

<h3 align="center"><mark>Examples</mark></h3>

<table align="center" style="border: 0.1px solid black;" width="1200px">
	<colgroup>
		<col span="1">
		<col span="1" style="background-color:rgb(0, 255, 128, 0.2)">
		<col span="1">
		<col span="1" style="background-color:rgb(0, 255, 128, 0.2)">
		<col span="1">
	</colgroup>
	<tbody>
		<tr>
			<th>&nbsp;</th>
			<th colspan="1">Given</th>
			<th colspan="1">Your Annotation</th>
			<th colspan="1">Given</th>
		</tr>
		<tr align="center">
			<th class="bb">&nbsp;</th>
			<th class="bb">Beginning</th>
			<th class="bb">What happened between the two parts?</th>
			<th class="bb">Ending</th>
		</tr>
		<tr>
			<td rowspan="1">1</td>
			<td>Hannah bought new headphones at the store.</td>
			<td><span style="color:#0000CD;"><b>She forgot her headphones at the store.</b></span></td>
			<td>She was disappointed by the quality of the headphones.</td>
		</tr>
		<tr>
			<td rowspan="1">2</td>
			<td class="bb">Hannah wanted a new pairs of headphones.</td>
			<td class="bb"><span style="color:#0000CD;"><b>She went to the store and they were out-of-stock.</b></span></td>
			<td class="bb">She was disappointed by the quality of the headphones.</td>
		</tr>
		<tr>
			<td rowspan="1">3</td>
			<td>Austin just got a new job and bought a new car.</td>
			<td><span style="color:#0000CD;"><b>He realized the car was cheap to maintain.</b></span></td>
			<td>He decided to look for a second job and have two incomes.</td>
		</tr>
		<tr>
			<td rowspan="1">4</td>
			<td>I went to buy groceries at the store.</td>
			<td><span style="color:#0000CD;"><b>I was the only one in line at the checkout counter.</b></span></td>
			<td>The person behind me in line paid for my groceries.</td>
		</tr>
	</tbody>
</table>

<h3 align="center"><mark>Tips and Rules</mark></h3>

<div style="width:800px; margin:0 auto;">
<ol>
	<li><u>General</u>

	<ul>
		<li>Input sentences must be <b>short</b> and have fewer than 10 words.</li>
		<li>Input sentences must be <b>simple</b>, as if narrating to a child.</li>
	</ul>
	</li>
	<li><u>Authoring the middle</u>
	<ul>
		<li><font color="red">Avoid</font> introducing any extraneous information.</li>
		<li>Use <font color="green"><b>names</b></font> instead of <font color="red">pronouns </font> (e.g. he / she) wherever possible.</li>
	</ul>
	</li>
</ol>
</div>

<hr>
<h3 align="center"><mark>Your Annotation</mark></h3>

<div style="width:1200px; margin:0 auto;">
<table align="center" border="0.1" width="1200px">
	<colgroup>
		<col span="1" style="background-color:rgb(0, 255, 128, 0.2)">
		<col span="1">
		<col span="1">
		<col span="1">
		<col span="1" style="background-color:rgb(0, 255, 128, 0.2)">
		<col span="1">
	</colgroup>
	<tbody>
		<tr align="center">
			<th>Beginning</th>
			<th>&nbsp;</th>
			<th width="30%">
			<p><span style="font-family:arial,helvetica,sans-serif;"><span style="color:#0000CD;">Write what happened between the 2 parts,<font size="2">&nbsp;preversing the narrative but making the story inconsistent.</font></span></span></p>
			</th>
			<th>&nbsp;</th>
			<th>Ending</th>
		</tr>
		<tr>
			<td>"Fred's boss called him into the office at the propane filling station."</td>
			<td align="center"><font size="100">→</font></td>
			<td><textarea cols="30" id="story1" name="story1" rows="4">Fred's boss started to yell at him.</textarea></td>
			<td align="center"><font size="100">→</font></td>
			<td>"Fred's boss gave him a large hug."</td>
		</tr>
		<tr>
		</tr>
	</tbody>
</table>
</div>

<p align="center"><input id="submitButton" type="submit" value="Submit"></p>

      
    </form>
  

</body></html>
""",
  os.path.join("img", "ex6.png"),
"self.actions.modify_text('story1', 'Fred's boss started to yell at him.')"
  ]

  instance_7 = [
"""
Input name: story1
HTML:
<html><head>
    <title>Task</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
  </head>
  <body>
    <form name="mturk_form" method="post" id="mturk_form" target="_parent" action="#">

      <input type="hidden" name="csrfmiddlewaretoken" value="DgFZAu4dD02keROuxCdZZDjXrDi86Fygn3HFg06gpxZDNJsqo9g12nUJw7YZBuOa">
      <style type="text/css">body {
													font-family: 'Helvetica', 'Arial', sans-serif;
													color: #444444;
													font-size: 12pt;
													background-color: #FAFAFA;
												}

												mark {
													background-color: rgb(153,50,204,0.3);
													color: black;
												}

												ul {
													text-align: left;
													list-style-position: inside;
												}

												textarea {
												font-size: 18px;
												margin: 0 auto;
												display: block;
												}

												#submitButton {
													font-size:20pt;
													color:white;
													background-color:green;
													border:2px solid #336600;
													padding:3px;
												}

											   table {
												   border-spacing: 5;
											   }

											   .bb {
												   border-bottom: 2px dotted black;
											   }
</style>
<h1 align="center"><span style="color:#FF8C00;">New Instructions: </span>Tweak a&nbsp;story to make it <span style="color:#0000CD;"><strong>implausible</strong></span></h1>

<h3 align="center"><span style="color:#FF8C00;">Please READ if you have not seen this symbol before: </span>â½</h3>

<h3 align="center"><mark>Overview</mark></h3>

<div style="width: 1000px; margin: 0px auto; text-align: center;">You will be shown a&nbsp;three-part story. Slightly modify the middle part so that it becomes&nbsp;<strong>inconsistent</strong>.</div>

<h3 align="center"><mark>Instructions</mark></h3>

<div style="width:1000px; margin:0 auto;">
<ol>
	<li>Review a&nbsp;<strong>three-part</strong> story. The beginning, middle,&nbsp;and&nbsp;ending of the story are given.</li>
	<li>Rewrite&nbsp;the&nbsp;<strong>middle</strong> with <strong>minimal changes</strong>, so that the whole story becomes<em>&nbsp;<strong>unlikely</strong></em>, <strong><em>improbable</em></strong>, or <strong><em>inconsistent</em></strong>.</li>
</ol>
</div>

<h3 align="center"><mark>Examples</mark></h3>

<table align="center" style="border: 0.1px solid black;" width="1200px">
	<colgroup>
		<col span="1">
		<col span="1" style="background-color:rgb(0, 255, 128, 0.2)">
		<col span="1">
		<col span="1" style="background-color:rgb(0, 255, 128, 0.2)">
		<col span="1">
	</colgroup>
	<tbody>
		<tr>
			<th>&nbsp;</th>
			<th colspan="1">Given</th>
			<th colspan="1">Your Annotation</th>
			<th colspan="1">Given</th>
		</tr>
		<tr align="center">
			<th class="bb">&nbsp;</th>
			<th class="bb">Beginning</th>
			<th class="bb">What happened between the two parts?</th>
			<th class="bb">Ending</th>
		</tr>
		<tr>
			<td rowspan="1">1.</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p>Lauren finished her late night shift at the bar feeling tired.</p>
			</td>
			<td>
			<p><span style="color:#FF8C00;"><strong>Original version:&nbsp;Lauren took a long hot bath when she got home.</strong></span></p>

			<p><span style="color:#0000CD;"><strong>Your version:&nbsp;Lauren's husband took a long hot bath when he got home.</strong></span></p>
			</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p>Lauren's husband was glad to see her feeling refreshed.</p>
			</td>
		</tr>
		<tr>
			<td rowspan="1">2.</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p>My mom was about to drive across a train track.</p>
			</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p><span style="color:#FF8C00;"><strong>Original version:&nbsp;My mom saw a train coming even though the gates were up.</strong></span></p>

			<p><strong>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			</strong></p>

			<p><strong><span style="color:#0000CD;">Your&nbsp;version:&nbsp;My mom saw a train coming even though the gates were down.</span></strong></p>
			</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p>My mom slammed on the brakes just in time.</p>
			</td>
		</tr>
		<tr>
			<td rowspan="1">3.</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p>Jessica hadn't seen her sister in months.</p>
			</td>
			<td>
			<p><span style="color:#FF8C00;"><strong>Original version: Jessica called her sister called and apologized.</strong></span></p>

			<p><span style="color:#0000CD;"><strong>Your version: Her sister called her and apologized.</strong></span></p>
			</td>
			<td>Her sister accepted her apology.</td>
		</tr>
		<tr>
			<td rowspan="1">4.</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p>Pablo wanted a jawbreaker.</p>
			</td>
			<td>
			<p><span style="color:#FF8C00;"><strong>Original version:&nbsp;Pablo checked his pockets for money.</strong></span></p>

			<p><span style="color:#0000CD;"><strong>Your version:&nbsp;Pablo checked his empty pockets for money.</strong></span></p>
			</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p>Then he bought his candy.</p>
			</td>
		</tr>
		<tr>
			<td>5.</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p>Ann loved cake.</p>
			</td>
			<td>
			<p><span style="color:#FF8C00;"><strong>Original version:&nbsp;The local baker offered Ann a job with no pay.</strong></span></p>

			<p><span style="color:#0000CD;"><strong>Your version:&nbsp;The local baker offered Ann a job with a good&nbsp;pay.</strong></span></p>
			</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p>Ann felt insulted by the lady's offer.</p>
			</td>
		</tr>
		<tr>
			<td>6.</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p>Jeffries's remote ran out of batteries.</p>
			</td>
			<td>
			<p><span style="color:#FF8C00;"><strong>Original version:&nbsp;It was the third time this month he had to buy batteries.</strong></span></p>

			<p><span style="color:#0000CD;"><strong>Your version:&nbsp;It was the first time in 10 years he had to buy batteries.</strong></span></p>
			</td>
			<td>
			<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
			</style>
			<p>He made sure to buy rechargeable batteries this time.</p>
			</td>
		</tr>
	</tbody>
</table>

<h3 align="center"><mark>Tips and Rules</mark></h3>

<div style="width:800px; margin:0 auto;">
<ol>
	<li><u>General</u>

	<ul>
		<li>Input sentences must <font color="green">minimally</font> alter the given middle.</li>
		<li>Add at most ~4&nbsp;new words to the story, and/or remove at most ~4 existing words.</li>
		<li>Your sentence should be <font color="green">grammatical</font> and syntactically correct.</li>
		<li>Stick to the <font color="green">context</font> of the given story. If the story talks about "doctors", you are welcome to talk about "health" or "diagnosis" for example, but don't mention "aliens".</li>
	</ul>
	</li>
	<li><u>Authoring the middle</u>
	<ul>
		<li><font color="red">Avoid</font> introducing any <span style="color:#FF0000;">extraneous</span> information.</li>
		<li>Use <font color="green">names</font> instead of <font color="red">pronouns </font> (e.g. he / she) wherever possible.</li>
		<li><font color="red">Avoid</font>&nbsp;simply <span style="color:#FF0000;">negating</span>&nbsp;the original version: "She likes cakes." -&gt; "She doesn't like cakes."&nbsp;</li>
	</ul>
	</li>
</ol>
</div>

<hr>
<h3 align="center"><mark>Your Annotation</mark></h3>

<div style="width:1200px; margin:0 auto;">
<table align="center" border="0.1" width="1200px">
	<colgroup>
		<col span="1" style="background-color:rgb(0, 255, 128, 0.2)">
		<col span="1">
		<col span="1">
		<col span="1">
		<col span="1" style="background-color:rgb(0, 255, 128, 0.2)">
		<col span="1">
	</colgroup>
	<tbody>
		<tr align="center">
			<th>Beginning</th>
			<th>&nbsp;</th>
			<th width="30%">
			<p><strong>Tweak the <span style="color:#FF8C00;">original middle</span>, making the<span style="color:#0000CD;"> whole story <u>inconsistent</u></span>.</strong></p>
			</th>
			<th>&nbsp;</th>
			<th>Ending</th>
		</tr>
		<tr>
			<td>"John loved to drive fast."</td>
			<td align="center"><font size="100">→</font></td>
			<td>
			<p>&nbsp;</p>

			<p><span style="color:#FF8C00;"><strong>Original middle:&nbsp;"John carelessly crashed into an elderly woman."</strong></span></p>

			<p><span style="color:#0000CD;"><strong>Your version:</strong></span></p>
			<textarea cols="30" id="story1" name="story1" required="" rows="4">He was a nascar driver.</textarea>

			<p><input id="InconsistentOriginalMiddle" name="InconsistentOriginalMiddle" type="checkbox" value="yes"><label for="InconsistentOriginalMiddle">&nbsp;The <span style="color:#FF8C00;">original middle</span> does <span style="color:#FF0000;">not</span> make a plausible story.</label></p>
			</td>
			<td align="center"><font size="100">→</font></td>
			<td>"John drove more carefully from then on."</td>
		</tr>
		<tr>
		</tr>
	</tbody>
</table>
</div>

<p><input id="InputStoryid" name="InputStoryid" type="hidden" value="" 1e425418-54d6-436b-9771-4fe9b7d99c65""=""> <input id="ending" name="ending" type="hidden" value="" -1""=""> <input id="GoldMiddle" name="GoldMiddle" type="hidden" value="" john="" carelessly="" crashed="" into="" an="" elderly="" woman.""=""> <input id="InputSentence1" name="InputSentence1" type="hidden" value="" john="" loved="" to="" drive="" fast.""=""> <input id="InputSentence2" name="InputSentence2" type="hidden" value="" one="" day,="" he="" was="" driving="" on="" an="" icy="" road.""=""> <input id="InputSentence3" name="InputSentence3" type="hidden" value="" he="" slid="" off="" the="" road="" and="" hit="" a="" tree.""=""> <input id="InputSentence4" name="InputSentence4" type="hidden" value="" he="" was="" okay,="" but="" his="" car="" wrecked.""=""> <input id="InputSentence5" name="InputSentence5" type="hidden" value="" john="" drove="" more="" carefully="" from="" then="" on.""=""> <input id="RandomMiddleSentenceQuiz1" name="RandomMiddleSentenceQuiz1" type="hidden" value="" undefined""=""> <input id="RandomMiddleSentenceQuiz2" name="RandomMiddleSentenceQuiz2" type="hidden" value="" john="" carelessly="" crashed="" into="" an="" elderly="" woman.""=""> <input id="CSK1" name="CSK1" type="hidden" value="" people="" learn="" from="" their="" mistakes.""=""> <input id="AnswerRightEnding" name="AnswerRightEnding" type="hidden" value="" 2""=""></p>

<p align="center"><input id="submitButton" type="submit" value="Submit"></p>
<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
</style>
<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
</style>
<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
</style>
<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
</style>
<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
</style>
<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
</style>
<style type="text/css">p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 11.0px Menlo; color: #000000}
span.s1 {font-variant-ligatures: no-common-ligatures}
</style>

      
    </form>
  

</body></html>
""",
  os.path.join("img", "ex7.png"),
"self.actions.modify_text('story1', 'He was a nascar driver.')"
  ]

  instance_8 = [
"""
Input name: radio0_9
HTML:
<html><head>
    <title>Task</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
  </head>
  <body>
    <form name="mturk_form" method="post" id="mturk_form" target="_parent" action="#">

      <input type="hidden" name="csrfmiddlewaretoken" value="CGWUi1FsA6BFSd0XZHoc8gA14NAFr5ADvWIVwT6Hc7pzDr7wlpNeO9Bwv2QEgbU8">
      <p><style type="text/css">
<!--
.odd {background: #E9CFEC;}
//-->
</style>
<link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"></p>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script> <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>
<table>
    <tbody>
        <tr>
            <td>
            <h1>Question Answering</h1>
            <p>You will be shown a question and several sentences that possibly answer the question.  Please judge  whether or not each of the sentences contains an answer to the question.</p>
            <ul>
                <li>To the right of each question we give a hint - a short phrase that is one possible correct answer.  This is not the only correct answer.</li>
                <li>The questions and sentences were created several years ago, so they may no longer be true.  You should still answer them as correct, if the text of the sentence gives a good answer that was true at that time.</li>
                <li>You do not need to look up whether each answer is correct.  Just say whether the sentence is a possible answer for the question.</li>
            </ul>
            <p>Here is one example:</p>
            <table>
                <tbody>
                    <tr class="odd">
                        <td colspan="2">Who is Tom Cruise married to?</td>
                        <td colspan="2"><b>Possible answer:</b> nicole kidman</td>
                    </tr>
                    <tr>
                        <th colspan="2">Does the following sentence answer the question:</th>
                        <td><b>Yes</b></td>
                        <td><b>No</b></td>
                    </tr>
                    <tr class="odd">
                        <td>1.</td>
                        <td>The film itself, starring Tom Cruise and Nicole Kidman as a married couple in New York on a sexual odyssey, received wildly mixed reviews.</td>
                        <td>&nbsp;</td>
                        <td><input type="radio" checked="checked"></td>
                    </tr>
                    <tr>
                        <td>2.</td>
                        <td>One of the world's most lusted-after men, Tom Cruise, is married to Nicole Kidman and her curls.</td>
                        <td><input type="radio" checked="checked"></td>
                        <td>&nbsp;</td>
                    </tr>
                    <tr class="odd">
                        <td>3.</td>
                        <td>The drama is said to be about a pair of married psychiatrists (played by the married Tom Cruise and Nicole Kidman) and their sexual lives, but only a few Warner executives, Cruise and Kidman, and Pat Kingsley, a top public relations executive, have seen the film .</td>
                        <td>&nbsp;</td>
                        <td><input type="radio" checked="checked"></td>
                    </tr>
                    <tr>
                        <td>4.</td>
                        <td>Now with the release of ``Eyes Wide Shut'' on DVD, everyone has a chance to give the film the look it deserves _ without the hype about sexual titillation or its married stars, Tom Cruise and Nicole Kidman .</td>
                        <td><input type="radio" checked="checked"></td>
                        <td>&nbsp;</td>
                    </tr>
                </tbody>
            </table>
            </td>
            <td bgcolor="#d3d3d3" valign="top"><font size="-2"><center><u><b>Informed Consent Form</b></u></center>
            <p><b>Purpose of research study:</b> We are collecting judgments about the quality of automatically generated text as part of our research into human language technologies.</p>
            <p><b>Benefits:</b> Although it will not directly benefit you, this study may benefit society by improving how computers process human languages. This could lead to better translation software, improved web searching, or new user interfaces for computers and mobile devices.</p>
            <p><b>Risks:</b>There are no risks for participating in this study.</p>
            <p><b>Voluntary participation:</b>You may stop participating at any time without penalty by clicking on the “Return HIT” button, or closing your browser window.</p>
            <p><b>We may end your participation if</b> you do not have adequate knowledge of the language, or you are not following the instructions, or your answers significantly deviate from known translations.</p>
            <p><b>Confidentiality: </b>The only identifying information kept about you will be a WorkerID serial number and your IP address. This information may be disclosed to other researchers.</p>
            <p><b>Questions/concerns: </b>You may e-mail questions to the principle investigator, <a href="http://cs.jhu.edu/~ccb/">Chris Callison-Burch</a>. If you feel you have been treated unfairly you may contact the Johns Hopkins University <a href="http://web.jhu.edu/Homewood-IRB/contact.html">Institutional Review Board</a>.</p>
            <p><b>Clicking on the “Accept HIT” button</b> indicates that you understand the information in this consent form. You have not waived any legal rights you otherwise would have as a participant in a research study.</p>
            </font></td>
        </tr>
    </tbody>
</table>
<table>
    <tbody>
        <tr class="odd">
            <td>
            <p><u><b>Notes:</b></u></p>
            <p><i>This was true in the past</i></p>
            Even though Cruise is not married to Kidman anymore, it was true in the past. Thus as long as the sentence suggests such a "fact", you should click the "Yes" button.             You'll see other similar examples in the HIT, such as asking whom the president of the U.S. is, and the answer is not necessarily Obama.             <br>
            <p><i>The possible answer is just a hint!</i></p>
            For each question, we provide some possible answers to help you. However, a sentence containing a hint <i>doesn't always mean it is a good answer</i> to the question.             For instance, sentence 1 above mentions Nicole Kidman, but it only suggests that Cruise and Kidman played a married couple in a movie (not real life), thus it does not answer the original question.</td>
        </tr>
    </tbody>
</table>
<script type="text/Javascript">

$(document).ready(function(){
  $("sth").hide();
  $('#second').click(function(){
    $('sth').toggle();
  });
});

$(document).ready(function(){
  $("sh").hide();
  $('#first').click(function(){
    $('sh').toggle();
  });
});

var questions = [
	"What is a fuel cell?",
	"What is the deepest lake in the US?",
	"What is pneumonia?"
    ];

var answers = [
	"electrochemical device electrical generators phosphoric acid molten carbon(ate)? hydrogen.*fuels? naphtha-based phosphate provide electrical power polymer electrolyte takes natural gas solid oxide use.*(butane|propane) hydrogen and oxygen converts gas to electricity proven technology convert combustible liquids chemical",
	"crater",
	"respiratory diseases? inflammation dangerous infection common cause of death most frequent killer of aids patients common killer of people common infections? most common aids - related influenza virus pneumocystis carinii infections? pneumococcus bacteria pcp caused by bacteria fatal complication life-threatening infect(ion)?"
    ];

var sentences = new Array();


sentences[0] = [
	"One such technology is the fuel cell&#44; which uses a chemical reaction to produce electricity from methanol&#44; natural gas or hydrogen.",
	"Fuel Cell Power    Heat Pumps               Superconductor Power          Ceramic Gas Turbine         Secondary Battery Generation                                  Applications Technology                                   Development Technology  Japan      Phosphoric acid    --In process of          Superconductive electrical    (For power                  Na/S&#44; Zn/Br batteries: fuel cells: Have   developing 1&#44;000kW       generator: Developing a 7kW   generation)Manufacturing    Completed development of developed basic    heat pump (super heat    model superconducting         a prototype of a 300kW      batteries for a 1&#44;000kW plant              pump).For heating        generator in line with        basic ceramic gas turbine   pilot plant (first in technologies.",
	"The fuel cell system consists of a hydrogen dissociation type reformer that directly manufactures very pure hydrogen from city gas (natural gas) and a solid polymer fuel cell manufactured by Mitsubishi Heavy Industries.",
	"R&amp;amp;D are progressing at present on three types of fuel cells&#44; namely: molten carbonate fuel cells (MCFC)&#44; solid oxide fuel cells (SOFC) and polymer electrolyte fuel cells (PEFC).",
    "Among the project&#39;s programs: huge new batteries that store power generated at night to sell during peak-demand daytime hours; &quot;fuel cells&quot; that use chemical reactions to turn fuels into electricity; and a new motor called the Stirling Cycle engine that runs on oil&#44; natural gas&#44; or coal and can power anything from air conditioners to buses.",
	"(A fuel cell takes natural gas -- or gas from garbage&#44; wood chips and other so-called biomass material -- and efficiently turns it into electricity through a chemical reaction.",
	"The company&#39;s solid oxide fuel cell has already been sold for testing purposes to Japanese natural gas companies.",
	"Polymer Electrolyte Fuel Cells (PEFC)                                     | ------------------------------------------------------------------------------- |Item                                               |1kW class module         | ------------------------------------------------------------------------------- |Output                                             |1kW                      | ------------------------------------------------------------------------------- |Fuel                                               |Hydrogen-air (pressurize-| |                                                   |d)                       | ------------------------------------------------------------------------------- |Average performance of cell                        |Initial characteristics 0| |                                                   |.3W/cm&amp;lt;sup&amp;gt; 2&amp;lt;/sup&amp;gt;        | -------------------------------------------------------------------------------   The present schedule calls for the development by fiscal 1995 of solid oxide fuel cells of several kilowatts&#44; which raises hope for an effective utilization of waste heat produced from high output density and high temperature operation in addition to the same excellent features as MCFC.",
	"Molten Carbonate Fuel Cells (MCFC)                                        | ------------------------------------------------------------------------------- |Item                     |1&#44;000kW Class System     |100kW Class Stack for In-| |                         |                         |termediate Evaluation    | ------------------------------------------------------------------------------- |Output                   |1&#44;000kW (AC)             |30-100kW                 | ------------------------------------------------------------------------------- |Power generation efficie-|Above 45%                |                         | |ncy                      |                         |                         | ------------------------------------------------------------------------------- |Fuel                     |LNG                      |Reformed natural gas or  | |                         |                         |coal gas (refined) (ordi-| |                         |                         |nary pressure or pressur-| |                         |                         |ized)                    | ------------------------------------------------------------------------------- |Environment load         |Below legal standard     |--                       | ------------------------------------------------------------------------------- |Average performance of c-|--                       |Initial characteristics 0| |ell                      |                         |.8 V/150 mA/cm&amp;lt;sup&amp;gt; 2     | |                         |                         |&amp;lt;/sup&amp;gt; Temporal deteriora-| |                         |                         |tion Below 1%/1&#44;000 hr   | ------------------------------------------------------------------------------- |2.",
    "Fuel cells&#44; which work at low temperatures and do not rely on the burning of fossil fuels&#44; produce no oxides of nitrogen or sulphur (the causes of acid rain)&#44; need no batteries which would have to be recharged or recycled and can obtain hydrogen from such different fuels as natural gas&#44; methanol&#44; biomass gas&#44; methane and other gases.",
    ];

sentences[1] = [
	"Crater Lake&#44; the nation&#39;s deepest _ 1&#44;932 feet _ and clearest lake&#44; was formed when the Mount Mazama volcano erupted about 6&#44;800 years ago and collapsed to form a gigantic bowl called a caldera.",
	" Scientists using a one-person submersible craft plan Wednesday to make the first of 20 dives looking for hot springs at the bottom of Crater Lake&#44; the deepest lake in the United States.",
	" An Oregon State University oceanographer piloting a one-man submarine has become the first person to see the bottom of Crater Lake&#44; the nation&#39;s deepest lake.",
	" A helicopter lifted a one-man submarine to Wizard Island in the prelude to man&#39;s first in-person look at the bottom of Crater Lake&#44; the deepest lake in the United States.",
    "``We found the temperatures we&#39;ve been looking for for three years&#44;&#39;&#39; said Crater Lake National Park biologist Jim Milestone.",
	"``It was very rough terrain down there&#44;&#39;&#39; said Jim Milestone&#44; natural resource management specialist for the National Park Service at Crater Lake.",
	"We chose Ruapehu&#44; which&#44; unusually&#44; has a lake in its crater.",
	"Wallace Stegner&#44; Pulitzer Prize-winning author of the novel &quot;Angle of Repose&quot; and of many volumes of Western history&#44; considers Crater Lake National Park in southwest Oregon&#44; established in 1915&#44; a classic of the genre.",
	"Timberline&#39;s bikers will visit 28 national parks and monuments during 1990&#44; including Yellowstone&#44; the Grand Tetons&#44; Glacier Bay&#44; Lucky Mountain&#44; Mesa Verde&#44; Grand Canyon&#44; Bryce&#44; Zion&#44; Canyonlands&#44; Crater Lake&#44; Mt.",
    "Three weeks of dives from Wizard Island were to begin today in the 1&#44;932-foot-deep lake&#44; the centerpiece of Crater Lake National Park in the Cascade Mountains.",
    ];

sentences[2] = [
	"PCP&#44; or pneumocystis carinii pneumonia&#44; is the most common AIDS-related infection and has been considered one of the most quickly fatal diseases that can overwhelm the damaged immune systems of people with AIDS.",
	"The most common cause of death in AIDS patients&#44; for example&#44; is a pneumonia caused by a microbe known as pneumocystis carinii&#44; which rarely afflicts healthy persons.",
	"     Since pneumonia can be caused by influenza virus&#44; pneumococcus bacteria or a variety of other infections&#44; you should get the flu and pneumonia vaccine if you are over 65&#44; a smoker and/or suffer from any chronic cardiovascular or respiratory condition.",
	"The aerosol drug approved in June is used to ward off pneumocystis carinii pneumonia&#44; the leading cause of death among AIDS patients.",
    "Since 1984&#44; Lyphomed has produced an injectable form of the drug for use in patients who already have contracted pneumocystis carinii pneumonia&#44; a life-threatening form of pneumonia that is the leading cause of death among AIDS patients.",
	"Prophylactic use of aerosol pentamidine can prevent PCP (Pneumocystis carinii pneumonia)&#44; a potentially lethal opportunistic infection for people with AIDS.",
	"Pollock became ill in December with his first bout of pneumocystis carinii pneumonia&#44; the most common killer of people with acquired immune deficiency syndrome&#44; which weakens a person&#39;s immune system and leaves them susceptible to numerous infections.",
	"Pneumocystis carinii pneumonia is the most common infection that kills AIDS patients.",
	"Pneumocystis carinii pneumonia is the most common infection that kills AIDS patients.",
    "Empire Blue Cross and Blue Shield of New York often goes to court to resist claims submitted by current policyholders&#44; arguing&#44; for example&#44; that a case of Kaposi&#39;s Sarcoma or pneumocystis carinii pneumonia&#44; both AIDS diseases&#44; indicates an uninsured &quot;pre-existing condition&quot; of AIDS virus infection.",
    ];



function randOrd(){
	return (Math.random()-0.5);
}

function checkedRadios() {
    if ($('input[type=radio]:checked').size() - 4 == ($('input[type=radio]').size() - 4) / 2) {
        return true;
    } else {
        alert("You have to finish all 30 judgement to submit!");
        return false;
    }
}

function showHide(showHideDiv, switchTextDiv1, switchTextDiv2) {
    var text = document.getElementById(showHideDiv);
    var ele1 = document.getElementById(switchTextDiv1);
    var ele2 = document.getElementById(switchTextDiv2);
    if(ele1.style.display == "inline") {
        ele1.style.display = "none";
        ele2.style.display = "none";
        text.innerHTML = "[more]";
    }
    else {
        ele1.style.display = "inline";
        ele2.style.display = "inline";
        text.innerHTML = "[hide]";
    }
}

function writeParaphraseTables() {

    // randomize the order
    var word_order = new Array(questions.length);
    for(var k = 0; k < word_order.length; k++) {
        word_order[k] = [k];
    }
    word_order.sort( randOrd );

	for(i0 = 0; i0 < questions.length; i0++) {
        i = word_order[i0];
		document.write('<p><table>');
        document.write('<tr>\n');
        document.write('<td colspan="2">' + questions[i] + '</td>');
        document.write('<td colspan="2"><b>Possible Answer:</b> ' + answers[i] + '</td>');
		document.write('</tr>');

        document.write('<tr><th colspan="2">Does the following sentence answer the question:</th><th>Yes</th><th>No</th></tr>');

		// randomize the order
		var order = new Array(sentences[i].length);
		for(var k = 0; k < order.length; k++) {
			order[k] = [k];
		}
		order.sort( randOrd );

		for(j0 = 0; j0 < order.length; j0++) {
            j = order[j0];
				document.write('<tr>');
				document.write('<td>' + (j0 + 1) + '. ' + '</td>');
				document.write('<td>'+sentences[i][j]+'</td>');
				document.write('<td align="center">');
			        document.write('<input type="radio" name="radio' + i + '_' + j + '" value="1">');
				document.write('</td>');
				document.write('<td align="center">')
			        document.write('<input type="radio" name="radio' + i + '_' + j + '" value="0">');
				document.write('</td>');
				document.write('</tr>');
		}
		document.write('</table></p>');
	}
}
writeParaphraseTables();
$("tr:odd").addClass("odd");
</script><p></p><table><tbody><tr>
<td colspan="2">What is a fuel cell?</td><td colspan="2"><b>Possible Answer:</b> electrochemical device electrical generators phosphoric acid molten carbon(ate)? hydrogen.*fuels? naphtha-based phosphate provide electrical power polymer electrolyte takes natural gas solid oxide use.*(butane|propane) hydrogen and oxygen converts gas to electricity proven technology convert combustible liquids chemical</td></tr><tr class="odd"><th colspan="2">Does the following sentence answer the question:</th><th>Yes</th><th>No</th></tr><tr><td>1. </td><td>Fuel cells, which work at low temperatures and do not rely on the burning of fossil fuels, produce no oxides of nitrogen or sulphur (the causes of acid rain), need no batteries which would have to be recharged or recycled and can obtain hydrogen from such different fuels as natural gas, methanol, biomass gas, methane and other gases.</td><td align="center"><input type="radio" name="radio0_9" value="1" checked=""></td><td align="center"><input type="radio" name="radio0_9" value="0"></td></tr><tr class="odd"><td>2. </td><td>The fuel cell system consists of a hydrogen dissociation type reformer that directly manufactures very pure hydrogen from city gas (natural gas) and a solid polymer fuel cell manufactured by Mitsubishi Heavy Industries.</td><td align="center"><input type="radio" name="radio0_2" value="1"></td><td align="center"><input type="radio" name="radio0_2" value="0"></td></tr><tr><td>3. </td><td>R&amp;amp;D are progressing at present on three types of fuel cells, namely: molten carbonate fuel cells (MCFC), solid oxide fuel cells (SOFC) and polymer electrolyte fuel cells (PEFC).</td><td align="center"><input type="radio" name="radio0_3" value="1"></td><td align="center"><input type="radio" name="radio0_3" value="0"></td></tr><tr class="odd"><td>4. </td><td>One such technology is the fuel cell, which uses a chemical reaction to produce electricity from methanol, natural gas or hydrogen.</td><td align="center"><input type="radio" name="radio0_0" value="1"></td><td align="center"><input type="radio" name="radio0_0" value="0"></td></tr><tr><td>5. </td><td>The company's solid oxide fuel cell has already been sold for testing purposes to Japanese natural gas companies.</td><td align="center"><input type="radio" name="radio0_6" value="1"></td><td align="center"><input type="radio" name="radio0_6" value="0"></td></tr><tr class="odd"><td>6. </td><td>Fuel Cell Power    Heat Pumps               Superconductor Power          Ceramic Gas Turbine         Secondary Battery Generation                                  Applications Technology                                   Development Technology  Japan      Phosphoric acid    --In process of          Superconductive electrical    (For power                  Na/S, Zn/Br batteries: fuel cells: Have   developing 1,000kW       generator: Developing a 7kW   generation)Manufacturing    Completed development of developed basic    heat pump (super heat    model superconducting         a prototype of a 300kW      batteries for a 1,000kW plant              pump).For heating        generator in line with        basic ceramic gas turbine   pilot plant (first in technologies.</td><td align="center"><input type="radio" name="radio0_1" value="1"></td><td align="center"><input type="radio" name="radio0_1" value="0"></td></tr><tr><td>7. </td><td>Among the project's programs: huge new batteries that store power generated at night to sell during peak-demand daytime hours; "fuel cells" that use chemical reactions to turn fuels into electricity; and a new motor called the Stirling Cycle engine that runs on oil, natural gas, or coal and can power anything from air conditioners to buses.</td><td align="center"><input type="radio" name="radio0_4" value="1"></td><td align="center"><input type="radio" name="radio0_4" value="0"></td></tr><tr class="odd"><td>8. </td><td>Polymer Electrolyte Fuel Cells (PEFC)                                     | ------------------------------------------------------------------------------- |Item                                               |1kW class module         | ------------------------------------------------------------------------------- |Output                                             |1kW                      | ------------------------------------------------------------------------------- |Fuel                                               |Hydrogen-air (pressurize-| |                                                   |d)                       | ------------------------------------------------------------------------------- |Average performance of cell                        |Initial characteristics 0| |                                                   |.3W/cm&amp;lt;sup&amp;gt; 2&amp;lt;/sup&amp;gt;        | -------------------------------------------------------------------------------   The present schedule calls for the development by fiscal 1995 of solid oxide fuel cells of several kilowatts, which raises hope for an effective utilization of waste heat produced from high output density and high temperature operation in addition to the same excellent features as MCFC.</td><td align="center"><input type="radio" name="radio0_7" value="1"></td><td align="center"><input type="radio" name="radio0_7" value="0"></td></tr><tr><td>9. </td><td>(A fuel cell takes natural gas -- or gas from garbage, wood chips and other so-called biomass material -- and efficiently turns it into electricity through a chemical reaction.</td><td align="center"><input type="radio" name="radio0_5" value="1"></td><td align="center"><input type="radio" name="radio0_5" value="0"></td></tr><tr class="odd"><td>10. </td><td>Molten Carbonate Fuel Cells (MCFC)                                        | ------------------------------------------------------------------------------- |Item                     |1,000kW Class System     |100kW Class Stack for In-| |                         |                         |termediate Evaluation    | ------------------------------------------------------------------------------- |Output                   |1,000kW (AC)             |30-100kW                 | ------------------------------------------------------------------------------- |Power generation efficie-|Above 45%                |                         | |ncy                      |                         |                         | ------------------------------------------------------------------------------- |Fuel                     |LNG                      |Reformed natural gas or  | |                         |                         |coal gas (refined) (ordi-| |                         |                         |nary pressure or pressur-| |                         |                         |ized)                    | ------------------------------------------------------------------------------- |Environment load         |Below legal standard     |--                       | ------------------------------------------------------------------------------- |Average performance of c-|--                       |Initial characteristics 0| |ell                      |                         |.8 V/150 mA/cm&amp;lt;sup&amp;gt; 2     | |                         |                         |&amp;lt;/sup&amp;gt; Temporal deteriora-| |                         |                         |tion Below 1%/1,000 hr   | ------------------------------------------------------------------------------- |2.</td><td align="center"><input type="radio" name="radio0_8" value="1"></td><td align="center"><input type="radio" name="radio0_8" value="0"></td></tr></tbody></table><p></p><p></p><table><tbody><tr>
<td colspan="2">What is the deepest lake in the US?</td><td colspan="2"><b>Possible Answer:</b> crater</td></tr><tr class="odd"><th colspan="2">Does the following sentence answer the question:</th><th>Yes</th><th>No</th></tr><tr><td>1. </td><td>Crater Lake, the nation's deepest _ 1,932 feet _ and clearest lake, was formed when the Mount Mazama volcano erupted about 6,800 years ago and collapsed to form a gigantic bowl called a caldera.</td><td align="center"><input type="radio" name="radio1_0" value="1"></td><td align="center"><input type="radio" name="radio1_0" value="0"></td></tr><tr class="odd"><td>2. </td><td>``It was very rough terrain down there,'' said Jim Milestone, natural resource management specialist for the National Park Service at Crater Lake.</td><td align="center"><input type="radio" name="radio1_5" value="1"></td><td align="center"><input type="radio" name="radio1_5" value="0"></td></tr><tr><td>3. </td><td> Scientists using a one-person submersible craft plan Wednesday to make the first of 20 dives looking for hot springs at the bottom of Crater Lake, the deepest lake in the United States.</td><td align="center"><input type="radio" name="radio1_1" value="1"></td><td align="center"><input type="radio" name="radio1_1" value="0"></td></tr><tr class="odd"><td>4. </td><td>Three weeks of dives from Wizard Island were to begin today in the 1,932-foot-deep lake, the centerpiece of Crater Lake National Park in the Cascade Mountains.</td><td align="center"><input type="radio" name="radio1_9" value="1"></td><td align="center"><input type="radio" name="radio1_9" value="0"></td></tr><tr><td>5. </td><td>Wallace Stegner, Pulitzer Prize-winning author of the novel "Angle of Repose" and of many volumes of Western history, considers Crater Lake National Park in southwest Oregon, established in 1915, a classic of the genre.</td><td align="center"><input type="radio" name="radio1_7" value="1"></td><td align="center"><input type="radio" name="radio1_7" value="0"></td></tr><tr class="odd"><td>6. </td><td>We chose Ruapehu, which, unusually, has a lake in its crater.</td><td align="center"><input type="radio" name="radio1_6" value="1"></td><td align="center"><input type="radio" name="radio1_6" value="0"></td></tr><tr><td>7. </td><td>``We found the temperatures we've been looking for for three years,'' said Crater Lake National Park biologist Jim Milestone.</td><td align="center"><input type="radio" name="radio1_4" value="1"></td><td align="center"><input type="radio" name="radio1_4" value="0"></td></tr><tr class="odd"><td>8. </td><td> An Oregon State University oceanographer piloting a one-man submarine has become the first person to see the bottom of Crater Lake, the nation's deepest lake.</td><td align="center"><input type="radio" name="radio1_2" value="1"></td><td align="center"><input type="radio" name="radio1_2" value="0"></td></tr><tr><td>9. </td><td>Timberline's bikers will visit 28 national parks and monuments during 1990, including Yellowstone, the Grand Tetons, Glacier Bay, Lucky Mountain, Mesa Verde, Grand Canyon, Bryce, Zion, Canyonlands, Crater Lake, Mt.</td><td align="center"><input type="radio" name="radio1_8" value="1"></td><td align="center"><input type="radio" name="radio1_8" value="0"></td></tr><tr class="odd"><td>10. </td><td> A helicopter lifted a one-man submarine to Wizard Island in the prelude to man's first in-person look at the bottom of Crater Lake, the deepest lake in the United States.</td><td align="center"><input type="radio" name="radio1_3" value="1"></td><td align="center"><input type="radio" name="radio1_3" value="0"></td></tr></tbody></table><p></p><p></p><table><tbody><tr>
<td colspan="2">What is pneumonia?</td><td colspan="2"><b>Possible Answer:</b> respiratory diseases? inflammation dangerous infection common cause of death most frequent killer of aids patients common killer of people common infections? most common aids - related influenza virus pneumocystis carinii infections? pneumococcus bacteria pcp caused by bacteria fatal complication life-threatening infect(ion)?</td></tr><tr class="odd"><th colspan="2">Does the following sentence answer the question:</th><th>Yes</th><th>No</th></tr><tr><td>1. </td><td>PCP, or pneumocystis carinii pneumonia, is the most common AIDS-related infection and has been considered one of the most quickly fatal diseases that can overwhelm the damaged immune systems of people with AIDS.</td><td align="center"><input type="radio" name="radio2_0" value="1"></td><td align="center"><input type="radio" name="radio2_0" value="0"></td></tr><tr class="odd"><td>2. </td><td>The aerosol drug approved in June is used to ward off pneumocystis carinii pneumonia, the leading cause of death among AIDS patients.</td><td align="center"><input type="radio" name="radio2_3" value="1"></td><td align="center"><input type="radio" name="radio2_3" value="0"></td></tr><tr><td>3. </td><td>Pneumocystis carinii pneumonia is the most common infection that kills AIDS patients.</td><td align="center"><input type="radio" name="radio2_8" value="1"></td><td align="center"><input type="radio" name="radio2_8" value="0"></td></tr><tr class="odd"><td>4. </td><td>Prophylactic use of aerosol pentamidine can prevent PCP (Pneumocystis carinii pneumonia), a potentially lethal opportunistic infection for people with AIDS.</td><td align="center"><input type="radio" name="radio2_5" value="1"></td><td align="center"><input type="radio" name="radio2_5" value="0"></td></tr><tr><td>5. </td><td>The most common cause of death in AIDS patients, for example, is a pneumonia caused by a microbe known as pneumocystis carinii, which rarely afflicts healthy persons.</td><td align="center"><input type="radio" name="radio2_1" value="1"></td><td align="center"><input type="radio" name="radio2_1" value="0"></td></tr><tr class="odd"><td>6. </td><td>     Since pneumonia can be caused by influenza virus, pneumococcus bacteria or a variety of other infections, you should get the flu and pneumonia vaccine if you are over 65, a smoker and/or suffer from any chronic cardiovascular or respiratory condition.</td><td align="center"><input type="radio" name="radio2_2" value="1"></td><td align="center"><input type="radio" name="radio2_2" value="0"></td></tr><tr><td>7. </td><td>Empire Blue Cross and Blue Shield of New York often goes to court to resist claims submitted by current policyholders, arguing, for example, that a case of Kaposi's Sarcoma or pneumocystis carinii pneumonia, both AIDS diseases, indicates an uninsured "pre-existing condition" of AIDS virus infection.</td><td align="center"><input type="radio" name="radio2_9" value="1"></td><td align="center"><input type="radio" name="radio2_9" value="0"></td></tr><tr class="odd"><td>8. </td><td>Since 1984, Lyphomed has produced an injectable form of the drug for use in patients who already have contracted pneumocystis carinii pneumonia, a life-threatening form of pneumonia that is the leading cause of death among AIDS patients.</td><td align="center"><input type="radio" name="radio2_4" value="1"></td><td align="center"><input type="radio" name="radio2_4" value="0"></td></tr><tr><td>9. </td><td>Pollock became ill in December with his first bout of pneumocystis carinii pneumonia, the most common killer of people with acquired immune deficiency syndrome, which weakens a person's immune system and leaves them susceptible to numerous infections.</td><td align="center"><input type="radio" name="radio2_6" value="1"></td><td align="center"><input type="radio" name="radio2_6" value="0"></td></tr><tr class="odd"><td>10. </td><td>Pneumocystis carinii pneumonia is the most common infection that kills AIDS patients.</td><td align="center"><input type="radio" name="radio2_7" value="1"></td><td align="center"><input type="radio" name="radio2_7" value="0"></td></tr></tbody></table><p></p>
<p>&nbsp;Please provide any comments that you have about this HIT. We appreciate your input!</p>
<p><textarea rows="4" cols="80" name="comment"> </textarea>&nbsp;</p>
<p>&nbsp;</p>
<p><input type="submit" value="Submit" onclick="return checkedRadios()" name="submitit"></p>
<p>&nbsp;</p>
<p><input type="hidden" name="userDisplayLanguage" value="en-US"> <input type="hidden" name="browserInfo" value="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/119.0.0.0 Safari/537.36"> <input type="hidden" name="ipAddress"> <input type="hidden" name="country" value="United States"> <input type="hidden" name="city" value="Pittsburgh"> <input type="hidden" name="region" value="Pennsylvania"></p>
<script language="Javascript" src="http://gd.geobytes.com/gd?after=-1&amp;variables=GeobytesCountry,GeobytesCity,GeobytesRegion,GeobytesIpAddress">
</script><script language="Javascript">
<!--
function getUserInfo() {
	var userDisplayLanguage = navigator.language ? navigator.language : navigator.userDisplayLanguage;
	var browserInfo = navigator.userAgent;
	var country = sGeobytesCountry;
	var city = sGeobytesCity;
	var region = sGeobytesRegion;

	document.mturk_form.userDisplayLanguage.value = userDisplayLanguage;
	document.mturk_form.browserInfo.value = browserInfo;
	document.mturk_form.country.value = country;
	document.mturk_form.city.value = city;
	document.mturk_form.region.value = region;
}

getUserInfo();

// -->
</script>

      
    </form>
  

</body></html>
""",
  os.path.join("img", "ex8.png"),
"self.actions.modify_radio('radio0_9', '1')"
  ]

  instance_9 = [
"""
Input name: norm
HTML:
<html lang="en"><head>
    <title>Task</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
  </head>
  <body>
    <form name="mturk_form" method="post" id="mturk_form" target="_parent" action="#">

      <input type="hidden" name="csrfmiddlewaretoken" value="jNrDgIQR1VnpJcwY08wLOLECm40X0wbFs1gmNkjmJ1ErToYQahUcPUAaZs7Ngzqt">
      
   <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

   <!-- BOOTSTRAP CSS -->
   <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
   <!-- HITPUB CSS -->
   <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i,700,700i" rel="stylesheet">
   <style id="hitpub_css">
      /***********************************************
      MOSAIC BOOSTRAP OVERWRITES
      ***********************************************/
      #hitinfo .card {
      border-radius: 0;
      }
      #hitinfo button.btn-link {
      color: #fff;
      text-decoration: none;
      }
      #hitinfo button.btn-link:hover {
      text-decoration: none;
      }
      #hit ul.question-choice {
      list-style-type: none;
      }
      /***********************************************
      MOSAIC GENERAL STYLING
      ***********************************************/
      body {
      font-family: "Open Sans", "Roboto", sans-serif;
      line-height: 1.25;
      }
      textarea#feedback {
      width: 100%
      }
      input#submitButton {
      margin: auto;
      display: block;
      /* background-color: #2172a4; */
      color: #fff;
      font-size: 1.125rem;
      padding: .5rem 1rem;
      cursor: pointer;
      border-radius: 1rem;
      }
      input#submitButton:hover {
      /* background-color: #06486F; */
      }
      input[type="radio"] {
      cursor: pointer;
      }
      div.question {
      border-bottom: solid 1px #ccc;
      padding: 1rem 0;
      }
      /***********************************************
      HIT CUSTOM GENERAL STYLING
      ***********************************************/
      div.card-header {
      /* background-color: #09545e; */
      background-color: #185dad;
      /* background-color: slateblue; */
      /* background-color: #e75858; */
      }
      div.card-header h5 {
      color: #fff !important;
      }
      li {
      margin: .5em 0;
      }
      label[for="2"]:hover, label[for="2"].active {
      background-color: #009300 !important;
      }
      label[for="1"]:hover, label[for="1"].active {
      background-color: #00b300 !important;
      }
      label[for="0"]:hover, label[for="0"].active {
      background-color: #999999 !important;
      }
      label[for="-1"]:hover, label[for="-1"].active {
      background-color:  #e30000 !important;
      }
      label[for="-2"]:hover, label[for="-2"].active {
      background-color: #9f0000 !important;
      }
      label[for="2"]:before, label[for="2"]:before {
      content:"strongly agree";
      }
      label[for="1"]:before, label[for="1"]:before {
      content:"moderately or weakly \A agree";
      white-space: pre;
      }
      label[for="0"]:before, label[for="0"]:before {
      content:"neither";
      white-space: pre;
      }
      label[for="-1"]:before, label[for="-1"]:before {
      content:"moderately or weakly  \A disagree";
      white-space: pre;}
      label[for="-2"]:before, label[for="-2"]:before {
      content:"strongly disagree";
      }
      .story-title {
      background-color: white;
      padding:2px;
      text-align: center;
      color: #333;
      }
      .beginning-title{
      background-color: #009E73;
      border: 2px double #009E73;
      color: white;
      }
      .ending-title{
      border: 2px double red;
      color: red;
      }
      .middle-title {
      border: 2px double #2393FF;
      color:#2393FF;
      }
      .story {
      border:1px solid #ccc;
      text-align: center;
      padding:10px;
      }
      .gray-out{
      background-color:#eee;
      color:white;
      border: 1px solid #eee;
      }
      .key-term {
      font-weight:bold;
      font-style:italic;
      }
      .key-term1{
      color: #4c6ef5;
      font-weight:bold;
      }
      .key-term2{
      color:#D55E00;
      font-weight:bold;
      }
      .key-term3{
      color: #27b183;
      font-weight:bold;
      }
      .key-term4{
      color: mediumvioletred;
      font-weight:bold;
      }
      .key-term5{
      color: goldenrod;
      font-weight:bold;
      }
      .key-term6{
      color: mediumslateblue;
      font-weight:bold;
      }
      .border-o1{
      border: 1px solid #009E73;
      }
      .border-o2 {
      border: 1px solid red;
      }
      .question-choice-container {
      padding-top:2em;
      border-top:1px solid #eee;
      }
      .question-choice-container label.btn {
      background-color: #eee;
      border: none;
      margin-left: 1 !important;
      color: black;
      font-size:95%;
      }
      .question-choice-container label.btn:hover {
      color: white;
      font-size:95%;
      }
      .example-choice-container label.btn {
      background-color: #ddd;
      border: 0;
      margin-left: 0 !important;
      color: black;
      font-size:95%;
      }
      label[for="btn_choice1"]:hover, label[for="btn_choice1"].active {
      background-color:  #fc6f00 !important;
      }
      .example-card {
      margin-top: 3em;
      }
      .legend {
      margin-top: .33rem;
      font-weight: normal;
      padding-left: 40px;
      }
      .legend .label{
      font-style: italic;
      }
      .emphasize {
      font-weight: bold;
      color: black;
      }
      .obj-emph {
      font-weight: bold;
      color: blue;
      }
      .use-emph{
      font-weight: bold;
      color: green;
      }
      .example {
      pointer-events:none;
      font-size:90%;
      }
      .goal {
      border-radius: .25rem;
      padding: 0.5rem 0.5rem;
      color: white;
      background-color: #555;
      transform: translateY(-20%);
      }
      @media (max-width:460px){
      body{
      display: none;
      }
      }
      .vbottom{
      position: relative;
      top: 100%;
      transform: translateY(50%);
      }
      .ht {
      border: 1px;
      color: white;
      background: #fc6f00;
      }
      /* facebook message bubbles */
      .imessage {
      background-color: #fff;
      border: 1px solid #fff;
      /* border: 1px solid #e5e5ea; */
      /* border-radius: 0.5rem; */
      display: flex;
      flex-direction: column;
      font-family: "SanFrancisco";
      font-size: 1.1rem;
      margin: 0 auto 1rem;
      padding: 0.5rem 0.5rem;
      }
      .imessage p {
      border-radius: 1.15rem;
      line-height: 1.25;
      max-width: 95%;
      padding: 0.5rem .875rem;
      position: relative;
      word-wrap: break-word;
      }
      .imessage p::before,
      .imessage p::after {
      bottom: -0.1rem;
      content: "";
      height: 1rem;
      position: absolute;
      }
      p.from-social {
      /* align-self: flex-end; */
      align-self: stretch;
      background-color: #FFE066;
      color: #000;
      }
      p.from-me {
      align-self: flex-end;
      /* background-color: #099268; */
      background-color: #10a276;
      color: #fff;
      }
      p.from-me::before {
      border-bottom-left-radius: 0.8rem 0.7rem;
      border-right: 1rem solid #10a276;
      right: -0.35rem;
      transform: translate(0, -0.1rem);
      }
      p.from-me::after {
      background-color: #fff;
      border-bottom-left-radius: 0.5rem;
      right: -40px;
      transform:translate(-30px, -2px);
      width: 10px;
      }
      p[class^="from-"] {
      margin: 0.5rem 0;
      width: fit-content;
      }
      p.from-me ~ p.from-me {
      margin: 0.25rem 0 0;
      }
      p.from-me ~ p.from-me:not(:last-child) {
      margin: 0.25rem 0 0;
      }
      p.from-me ~ p.from-me:last-child {
      margin-bottom: 0.5rem;
      }
      p.from-them {
      align-items: flex-start;
      background-color: #e5e5ea;
      color: #000;
      }
      p.from-them:before {
      border-bottom-right-radius: 0.8rem 0.7rem;
      border-left: 1rem solid #e5e5ea;
      left: -0.35rem;
      transform: translate(0, -0.1rem);
      }
      p.from-them::after {
      background-color: #fff;
      border-bottom-right-radius: 0.5rem;
      left: 20px;
      transform: translate(-30px, -2px);
      width: 10px;
      }
      p[class^="from-"].emoji {
      background: none;
      font-size: 2.5rem;
      }
      p[class^="from-"].emoji::before {
      content: none;
      }
      .no-tail::before {
      display: none;
      }
      .margin-b_none {
      margin-bottom: 0 !important;
      }
      .margin-b_one {
      margin-bottom: 1rem !important;
      }
      .margin-t_one {
      margin-top: 1rem !important;
      }
      input.form-check-input {
      padding-right: 10px;
      }
      ul>li:before{
      margin-left: -1em;
      margin-right: .25em;
      }
      ul>li.corr:before {
      content: "\2713";
      }
      ul>li.inco:before {
      content: "\2717";
      }
      input.form-check-input.right:after {
      /*
      position: absolute;
      bottom: 0;
      left: .5em;
      right: 0;
      content: "";
      height: 0.75em;
      border-top: 1px solid black;*/
      }
      .form-check.invalid,
      .lickert.invalid,
      input.invalid,
      select.invalid {
      border: .1em solid #D22437;
      border-radius: .1em;
      background-color: #f5c6cb;
      padding: .1em;
      }
   </style>
   <!-- LIGHTBOX CSS -->
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.1/css/lightbox.min.css">
   <!-- HIT START -->
   <div id="hit" class="container">
      <!-- ACCORDION START -->
      <div class="col-12 accordion" id="hitinfo">
         <!-- INSTRUCTIONS START -->
         <div class="card">
            <div class="card-header id=" instructionsheading"="">
               <h5 class="mb-0">
                  <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#instructions" aria-expanded="true" aria-controls="instructions">
                  Instructions (click to expand/collapse) <span class="emoji-bytes" data-emoji-bytes="[240, 159, 142, 132]">🎄</span><span class="emoji-bytes" data-emoji-bytes="[240, 159, 140, 159]">🌟</span>
                  </button>
               </h5>
            </div>
            <!-- <div class="collapse show" id="instructions" aria-labelledby="instructionsHeading" data-parent="#hitinfo"> -->
            <div class="collapse" id="instructions" aria-labelledby="instructionsHeading" data-parent="#hitinfo">
               <div class="card-body">
                  <div class="card-content">
                     <p>
                        <span class="emoji-bytes" data-emoji-bytes="[240, 159, 140, 159]">🌟</span> Happy New Year! Thanks for participating in this HIT! <span class="emoji-bytes" data-emoji-bytes="[240, 159, 140, 159]">🌟</span>
                     </p>
                     <p>We are glad that you are also participating in our dialogue project in the new year :)</p>
                     <p>â&nbsp;ï¸ <strong>The guidelines have been updated in the new year! Please read through the rules and examples carefully in your first try!</strong></p>
                     <div class="border pt-2 pl-2 pr-2 bg-light">
                        <p>Notes about this HIT</p>
                        <ul>
                           <!-- <li><strong>IF you have already taken this quals</strong>, please do NOT take it again. Only 1 will count. </li> -->
                           <li>In this HIT, you will be presented with a dialogue and some rules-of-thumb to select.</li>
                           <li>You will first modify the dialogue to be more fluent and coherent.</li>
                           <li>Then you will continue the dialogue by writing a response reflecting the rule-of-thumb you wrote or selected.</li>
                           <li>We expect this HIT to take about two and a half minutes.</li>
                           <li>Please read the instructions and the examples carefully.</li>
                              <!-- <li>If you are among the few who have worked on the pilot for task, make sure you still read the instructions as there are some <u>key differences</u> from the pilot. -->
                           <li><span class="badge badge-danger">Warning</span> This HIT may contain <strong>adult content</strong> and may be <strong>offensive</strong> or <strong>upsetting.</strong> <span class="key-term3">Worker discretion is strongly advised.</span></li>
                        </ul>
                     </div>
                     <h5 class="border-top pt-2">Your task:</h5>
                     <p>In this task, we are asking you to <strong>read a short conversation</strong> that mentions rude or unethical behavior and
                        <strong>type a response that gently <i>guide the speaker to be more prosocial</i></strong>, using <strong>rules-of-thumb</strong>.
                     </p>
                     <p>Outline of the task:</p>
                     <ol>
                        <!-- <li><span class="badge" style="background-color: #7950f2; color: white;">new!</span> Given a conversation, please <strong>modify the conversation to make it more fluent and coherent.</strong></li> -->
                        <li>Given a conversation, please <strong>modify the conversation to make it more fluent and coherent.</strong></li>
                        <li>Please <strong>write what you would say as a response</strong> to the conversation you modified, <b>using the rules-of-thumb to guide the other speaker to be more prosocial</b> (<span class="key-term1">conforming to more socially accepted behaviors</span>).
                        </li><li><strong>Write or select the most appropriate rules-of-thumb</strong> implied in your response.</li>
                     </ol>
                     
                     <p>Five example dialogues are given below the instruction panel.</p>
                     <h5 class="border-top pt-2">Rules:</h5>
                     <ul>
                        <li>For  <span class="key-term">utterance modification</span>: </li>
                        <ul>
                           <li>Please modify the utterances of the given conversation to make it more coherent and human-like.</li>
                           <li>If all utterances are coherent, you can also add your personal feelings such as "<em>Oh dear, I can't believe what you are saying</em>".</li>
                              <!-- <ul>
                                 <li>We encourage you to use "I-statements" (<a href="https://en.wikipedia.org/wiki/I-message">wikipedia</a>), an effective communication skill for preventing conflict escalation. By focusing on our feeling rather than accusing the speaker with "You-statements", we can make the dialogue smoother.</li>
                              </ul> -->
                           <li><span class="badge badge-warning">Important!</span> Especially check whether the <strong>last utterance</strong> is coherent to the dialogue and modify it.</li>
                              <ul>
                                 <li>If you think it is nonsensical, you can modify it the way you like, but it still has to be coherent to the dialogue.</li>
                              </ul>
                           <li><span class="badge badge-primary">Note!</span> If the <strong>second or fourth utterance</strong> is not socially acceptable, please modify it.</li>
                        </ul>
                        <li>For <span class="key-term">response annotation</span>: </li>
                        <ul>
                           <li>Write a response which guides the other speaker to be more prosocial (conforming to more socially acceptable behaviors).</li>
                           <strong>If the speaker's behavior is <span class="badge badge-warning">problematic</span> (e.g., disturbing, unethical, rude, biased, dangerous) and:</strong>
                           <ul>
                              <li>
                                 if the other speaker <span class="badge badge-danger">rejects</span> the critique <strong>â guide the speaker to be more prosocial</strong> (conform to more socially accepted behaviors):
                                 <ul>
                                    <li><i><u>Some tips</u></i>:</li>
                                    <li>Kindly suggest or wisely advise the speaker to <u>do more socially accepted behaviors</u></li>
                                    <li>Let the speaker know about the better alternate results when doing more socially accepted behaviors</li>
                                    <li>The art of persuasion is in making the other also want what you want, not making them do what you want</li>
                                 </ul>
                                    â "<i>Don't you also want to have a happy relationship with your family? How about a nice dinner with your parent rather then shouting?</i>"
                              </li>
                              <li>
                                 if the other speaker <span class="badge badge-primary">accepts</span> the critique and agrees to behave good <strong>â compliment their behavior :)</strong>
                                 <ul>
                                    <li><i><u>Some tips</u></i>:</li>
                                    <li>Tell the speaker it was a good decision to make</li>
                                    <li>Let them know it will lead to better results (e.g., friends or families will like it)</li>
                                 </ul>
                              </li>
                                 â "<i>I'm glad to hear that. I'm sure your friend will feel better regarding the accident.</i>"
                           </ul>
                           <br>
                           If the speaker's behavior was <span class="badge badge-success">safe</span> in the first place and nothing is problematic at all <strong>â freely continue the dialogue in a gentle manner</strong>
                           <ul>
                              <li>Ask questions or empathize or relate to your experience. </li>
                           </ul>

                           <!-- <li>Write a response which constructively critiques the unethical or rude behavior of the speaker.</li>
                           <li>The response should reflect both context-specific information and the rules-of-thumb you selected.</li>
                           <li>Don't hesitate to disagree with the previous conversation utterance!</li>
                           <li><span class="badge badge-warning">note!</span> Paraphrase the provided rule-of-thumb in your response, as long as it makes sense.</li>
                           <li>Do think about what would be considered rude or unethical in general American society, and make sure to <em>disagree with statements that are biased against minorities.</em></li>
                           <li><span class="badge badge-danger">NEW!</span> <strong>We recommend you follow the DOs and DON'Ts below:</strong> <span class="badge badge-danger">NEW!</span></li>
                           <ul>
                              <li>
                                 <strong>DOs</strong>
                                    <ul>
                                       <li>Stay <strong>calm</strong> and maintain a <strong>positive tone</strong></li>
                                       <li><strong>Label the comment</strong>, not the person. Example: "<em>Those words come from a racist stereotype.</em>"</li>
                                       <li><strong>Respect cultural differences</strong></li>
                                       <li><strong>Point out hasty generalization</strong></li>
                                       <li><strong>Encourage putting oneself in other people's shoes</strong></li>
                                       <li><span class="badge badge-success">Note!</span> <strong>Gently guide what the other should do instead to be socially acceptable</strong> (e.g., <em>learn about it by reading or watching useful resources</em>). This can help de-escalate the conflict. Example: "<em class='key-term3'>I heard that there's a nice Netflix show about it. Why don't you give it a try to learn about them more?</em>"</li>
                                       <li><strong>Refer to potential outcomes of such hate speech</strong> Example: "<em>That could hurt someone, You might be in a similar situation someday.</em>"</li>
                                       <li><strong>Include context-specific information and rules-of-thumb</strong></li>
                                       <li>Write about <span class="key-term">two ~ three</span> sentences. (four is also okay if it's not too long)</li>
                                    </ul>
                              </li>
                              <li>
                                 <strong>DON'Ts</strong>
                                    <ul>
                                       <li><strong>Don't label the speaker</strong> - for example, <em>calling them a bigot.</em></li>
                                       <li><strong>Don't be hostile, insulting, or aggressive</strong>, it can escalate the conflict.</li>
                                       <li><strong>Don't talk down to the speaker</strong></li>
                                       <li><strong>Don't write responses that are too general</strong> - for example, "<em>Don't say that.</em>"</li>
                                    </ul>
                              </li>
                           </ul> -->
                           <!-- â³ A good example response: <em style="color:mediumvioletred">I see you are fond of him,</em>  <em style="color:goldenrod">but you already have a boyfriend. You shouldn't seduce someone else,</em> <em style="color:mediumslateblue">he will be heartbroken.</em> <em style="color: #27b183">How about going somewhere with your boyfriend this weekend for a change?</em> </li> -->
                        </ul>
                        <li>For  <span class="key-term">rule-of-thumb annotation</span>: </li>
                        <ul>
                           <li>Please write or select the rule-of-thumb that you actually reflected in the response you wrote.</li>
                           <!-- <li><span class="badge badge-success">Note!</span> If nothing is problematic (unethical, rude, biased, disturbing, dangerous) with the speaker, select the <b>[no RoT needed]</b> option</li>
                           <ul>
                              <li><u><i>this inlcudes</i></u>:</li>
                              <li>the speaker willingly accepted the critique in the previous utterance</li>
                              <li>the problematic issue has been resolved</li>
                           </ul> -->

                           <!-- <li>Write a suitable rule-of-thumb for critiquing the other speaker in the dialogue.</li>
                           <li>The rules-of-thumb will be the ingredients of the response you will write for the dialogue you modified.</li>
                           <li>Write or choose appropriate ones for your response to the dialogue context.</li>
                           <li>You are free to choose multiple rules-of-thumb. Just make sure you reflect <em>all of them</em> in your response.</li>
                           <li><span class="badge badge-danger">NEW!</span> <strong>If there are multiple rules-of-thumb that basically mean the same thing, select just one.</strong></li> -->
                        </ul>
                        <li><strong class="key-term3">Please read through the examples below!</strong></li>
                        <!-- <li>If you want to learn more on how to give effective counterspeech, you can check out the <a href="https://dangerousspeech.org/wp-content/uploads/2016/10/Considerations-for-Successful-Counterspeech.pdf">https://dangerousspeech.org</a>! </li> -->
                     </ul>
                     <h5 class="border-top pt-2">Background on our research project:</h5>
                     <p><small>At the Allen Institute for AI, we are interested in creating conversational AI systems that can make the world better. We are very thankful for your help in creating datasets of example conversations that are not afraid to point out unethical or rude behavior, so that AI systems can learn to avoid unethical and rude behavior, and learn to call such behavior out.
                        We do not agree with any of the rude, unethical, or offensive content presented to you, but it's important that we gather these annotations for research purposes so that our AI systems can learn.</small>
                     </p>
                     <p><strong>Data collection &amp; sharing</strong><br>
                        <small>We will not ask you for your name, and the data collected in this study will be made unidentifiable to the best of our extent. We will securely store the data on our servers and only share with qualified researchers. If you later decide that you do not want your responses included in this study, please email so we can exclude your work.<br>
                        If you have questions about your rights as a research participant, or wish to obtain information, ask questions or discuss any concerns about this study with someone other than the researcher(s),
                        please contact the AI2 Institutional Review Board at <a href="mailto:irb@allenai.org">irb@allenai.org</a>.</small>
                     </p>
                     <p><span class="badge badge-danger">Content Warning</span><small> The conversation context is generated from a conversational AI system (a chatbot). It may contain rude, toxic, or offensive language and behavior. while it's crucial for us to annotate response against them, we do not endorse any of the stereotypes or offensive/immoral/rude material.
                        You may find some of the content upsetting. In such cases, <strong>you are free to return any HITs that make you uncomfortable</strong>. If you have concerns, questions, or strong negative reactions to some of the content, please email us (<a href="mailto:hyunwook@allenai.org">hyunwook@allenai.org</a>)
                        </small>
                     </p>
                     <p><small>Please take care of yourself! Some of these conversations could be very hard to read, so do not hesitate to take regular breaks. If some content is too upsetting and you are in crisis, please reach out to the <a href="https://www.crisistextline.org/">Crisis text line</a> or other mental health resources. </small></p>
                  </div>
               </div>
            </div>
         </div>
         <div class="card">
            <div class="card-header" id="exampleHeading" style="background-color: #099268">
               <h5 class="mb-0">
                  <button class="btn btn-link collapsed" type="button" data-toggle="collapse" data-target="#examples" aria-expanded="false" aria-controls="examples">
                  <!-- <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#examples" aria-expanded="true" aria-controls="examples"> -->
                  <!-- <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#instructions" aria-expanded="true" aria-controls="instructions"> -->
                  Examples of rule-of-thumb selection and response annotation (click to expand/collapse) <span class="emoji-bytes" data-emoji-bytes="[240, 159, 146, 171]">💫</span>
                  </button>
               </h5>
            </div>
            <!-- <div class="collapse show" id="examples" aria-labelledby="exampleheading" data-parent="#hitinfo"> -->
            <div class="collapse" id="examples" aria-labelledby="exampleheading" data-parent="#hitinfo">
               <div class="card-body">
                  <div class="card-content">
                     <div class="row border-bottom mb-3">
                        <h5 class="col col-12 bg-dark text-light">Example 1</h5>
                        <div class="card-group">
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Modified dialogue</h5>
                                 <div class="imessage">
                                    <p class="from-them">I passed my calc course because I smashed the professor.</p>
                                    <p class="from-me">What made you have sex with your professor?</p>
                                    <p class="from-them">The professor was a cute guy and I liked him a lot</p>
                                    <p class="from-me">I'm happy you had a good time with him. However, it was wrong of him and a serious dereliction of his duty to sleep with a student like that.  He could end up getting himself fired if you two continue.</p>
                                    <p class="from-them">He's a smart guy, he knows what he's doing. Plus, he cheated on his wife for me.</p>
                                 </div>
                              </div>
                           </div>
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Expected response annotation</h5>
                                 <div class="imessage">
                                    <p class="from-me">I believe it is wise to stop this relationship. Think of his family, how would they feel if they find out?</p>
                                 </div>
                              </div>
                           </div>
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Rule-of-thumb</h5>
                                 <div class="imessage">
                                    <p class="from-social no-tail"><span>â</span> <strong>[New RoTs are implied]</strong><br>itâs wrong to make someone cheat on his wife</p>
                                    <p class="from-social no-tail"><strong>[Previously selected RoTs are implied]</strong><br>it's wrong to sleep with your student</p>
                                    <!-- <p class="from-social no-tail"><strong>[Nothing problematic, no RoT needed]</strong></p> -->
                                 </div>
                              </div>
                           </div>
                        </div>
                     </div>
                     <div class="row border-bottom mb-3">
                        <h5 class="col col-12 bg-dark text-light">Example 2</h5>
                        <div class="card-group">
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Modified dialogue</h5>
                                 <div class="imessage">
                                    <p class="from-them">I'm going to miss my brother's wedding</p>
                                    <p class="from-me">Why? Weddings are important!</p>
                                    <p class="from-them">I just don't think I'll enjoy that very much.</p>
                                    <p class="from-me">It is an important family event! You should do your best to make it. It doesn't matter if you will enjoy it or not.</p>
                                    <p class="from-them">I'm sure my brother wants me there, but I will simply visit you afterwards. I no longer wish to attend the wedding.</p>
                                 </div>
                              </div>
                           </div>
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Expected response annotation</h5>
                                 <div class="imessage">
                                    <p class="from-me">Donât you want to make good memories too? When you take some photos and eat delicious banquet food, you'll probably find yourself enjoying the wedding!</p>
                                 </div>
                              </div>
                           </div>
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Rule-of-thumb</h5>
                                 <div class="imessage">
                                    <p class="from-social no-tail"><strong>[New RoTs are implied]</strong></p>
                                    <p class="from-social no-tail"><span>â</span> <strong>[Previously selected RoTs are implied]</strong><br>It is important that you participate in family event.</p>
                                    <!-- <p class="from-social no-tail"><strong>[Nothing problematic, no RoT needed]</strong></p> -->
                                 </div>
                              </div>
                           </div>
                        </div>
                     </div>
                     <div class="row  border-bottom mb-3">
                        <h5 class="col col-12 bg-dark text-light">Example 3</h5>
                        <div class="card-group">
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Modified dialogue</h5>
                                 <div class="imessage">
                                    <!-- Situation ID:  32991 -->
                                    <p class="from-them">I'm not who my family thinks I am.</p>
                                    <p class="from-me">Why do you hide youself from your family?</p>
                                    <p class="from-them">They are so controlling. I hate them for that.</p>
                                    <p class="from-me">You should be able to be yourself. If it won't affect you too negatively, you should be yourself around your family. You will end up happier in the end.</p>
                                    <p class="from-them">Yeah maybe I should.</p>
                                 </div>
                              </div>
                           </div>
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Expected response annotation</h5>
                                 <div class="imessage">
                                    <p class="from-me">Glad to hear that! You will start feeling more confident when you try to be yourself and probably this will help you with your relationship with your family too.</p>
                                 </div>
                              </div>
                           </div>
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Rule-of-thumb</h5>
                                 <div class="imessage">
                                    <p class="from-social no-tail"><strong>[New RoTs are implied]</strong></p>
                                    <p class="from-social no-tail"><span>â</span> <strong>[Previously selected RoTs are implied]</strong><br>It's ok to be yourself in front of people</p>
                                    <!-- <p class="from-social no-tail"><span>â</span> <strong>[Nothing problematic, no RoT needed]</strong></p> -->
                                 </div>
                              </div>
                           </div>
                        </div>
                     </div>
                     <div class="row  border-bottom mb-3">
                        <h5 class="col col-12 bg-dark text-light">Example 4</h5>
                        <div class="card-group">
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Modified dialogue</h5>
                                 <div class="imessage">
                                    <p class="from-them">I'm going to ask my sister not to open new credit card accounts</p>
                                    <p class="from-me">Is there a reason why you don't want your sister to open new credit card accounts?</p>
                                    <p class="from-them">I think she is too impulsive, at least more than me.</p>
                                    <p class="from-me">While a person's finances is their own business, it is also important to look out for the well-being of a family member. If you think your sister is being irresponsible with credit card debt, then it is okay for you to talk to her and warn her of the repercussions of falling into debt.</p>
                                    <p class="from-them">Actually, I want her to suffer from the financial aftermath.</p>
                                 </div>
                              </div>
                           </div>
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Expected response annotation</h5>
                                 <div class="imessage">
                                    <p class="from-me">I thought you were worrying about your sister! Even if you are trying to teach her a lesson, making her suffer is too much. </p>
                                 </div>
                              </div>
                           </div>
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Rule-of-thumb</h5>
                                 <div class="imessage">
                                    <p class="from-social no-tail"><span>â</span> <strong>[New RoTs are implied] </strong><br>It's wrong to make familiy member suffer from financial problem</p>
                                    <p class="from-social no-tail"><strong>[Previously selected RoTs are implied]</strong><br>It's ok to protect family members for their well-being</p>
                                    <!-- <p class="from-social no-tail"><strong>[Nothing problematic, no RoT needed]</strong></p> -->
                                 </div>
                              </div>
                           </div>
                        </div>
                     </div>
                     <div class="row  border-bottom mb-3">
                        <h5 class="col col-12 bg-dark text-light">Example 5</h5>
                        <div class="card-group">
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Modified dialogue</h5>
                                 <div class="imessage">
                                    <!-- situation id: 33760 -->
                                    <p class="from-them">I think my sister is too hot and it's affecting our relationship</p>
                                    <p class="from-me">How is it affecting your relationship with her?</p>
                                    <p class="from-them">I find it too hard to get intimate with her. She's such a sexy girl and I can't keep my eyes off her</p>
                                    <p class="from-me">It's gross to be attracted to your sister. You should only be attracted to people outside of your family.</p>
                                    <p class="from-them">Are you saying my sister is not attractive?</p>
                                 </div>
                              </div>
                           </div>
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Expected response annotation</h5>
                                 <div class="imessage">
                                    <p class="from-me">It doesnât matter whether your sister is attractive or not. All Iâm suggesting is to look for someone who is not your family for romantic relationships, perhaps friends at school?</p>
                                 </div>
                              </div>
                           </div>
                           <div class="card">
                              <div class="card-body">
                                 <h5 class="card-title">Rule-of-thumb</h5>
                                 <div class="imessage">
                                    <p class="from-social no-tail"><strong>[New RoTs are implied] </strong></p>
                                    <p class="from-social no-tail"><span>â</span> <strong>[Previously selected RoTs are implied]</strong><br>itâs wrong to be sexually attracted to family members.</p>
                                    <!-- <p class="from-social no-tail"><strong>[Nothing problematic, no RoT needed]</strong></p> -->
                                 </div>
                              </div>
                           </div>
                        </div>
                     </div>
                  </div>
               </div>
            </div>
         </div>
         <!-- INSTRUCTIONS END -->
      </div>
      <!-- ACCORDION END -->
      <!-- MTURK INPUT START -->
      <div class="row justify-content-center" id="consent-div">
         <div class="col-12 mt-4" style="text-align: center;">
            <h4>Consent to the task</h4>
            <div class="form-check" style="text-align: center"><label class="form-check-label" for="consent"><input checked="checked" class="form-check-input" id="consent" name="consent" onclick="toggleConsent(this.checked)" required="" type="checkbox"> By ticking this box, you certify that you have <strong>understood</strong> and <strong>agree</strong> with the terms of this study. </label></div>
            &nbsp;
            <div class="col col-12 p-1 mb-2 bg-warning" id="consent-message"><span style="font-size:100%">You must check the box to continue the task!</span></div>
         </div>
      </div>
      <div class="col-12 mt-5 mb-1 border-top" id="main-task">
         
         <!--<form name='mturk_form' method='post' id='mturk_form' > -->
            <input type="hidden" value="" name="assignmentId" id="assignmentId">
            <input type="hidden" name="ee" id="ee">

         <div id="question" class="row mb-3 question-choice-container">
            <div class="col col-12 p-2 mb-2 text-white" style="background-color: #3a4299"><span style="font-size:140%">Make the dialogue more coherent by modifying the utterances âï¸<span class="emoji-bytes" data-emoji-bytes="[240, 159, 140, 159]">🌟</span></span></div>
            <!-- <p class="text-body">Please choose the most coherent and human-like conversation that you will continue.</p> -->
            <div class="card-group col-12">
               <div class="card">
                  <div class="card-body">
                     <h5 class="card-title">Dialogue context</h5>
                     <p class="card-text">
                     </p><div class="imessage">
                        <p class="from-them" id="context1">I poured the hot coffee on the customer</p>
                        <p class="from-me" id="context2">Where were you when you did this? It doesn't sound like something you would do.</p>
                        <p class="from-them" id="context3">The customer made me mad.</p>
                        <p class="from-me" id="context4">It is not okay to pour coffee on someone on purpose.  It is especially not okay to do this at work.</p>
                        <p class="from-them" id="context5">The customer was an asshole, every day he complains about something.</p>
                     </div>
                     <p></p>
                  </div>
               </div>
               <div class="card col-6">
                  <div class="card-body">
                     <!-- <h5 class="card-title">Modify the utterances for better coherency</h5> -->
                     <p class="card-text">
                     </p><ul>
                        <li>For utterance that does not need any modification, you can leave the input form as a blank.</li>
                        <!-- <li>When all utterances are natural and human-like, we recommend you to modify the <strong>last utterance</strong> to be coherent.</li>  -->
                        <li><span class="badge badge-warning">Important!</span> Please modify the <strong>last utterance</strong> to be coherent to the dialogue and modify it. If you think it is nonsensical, you can modify it the way you like.</li>
                        <li><span class="badge badge-primary">Note!</span> If the <strong>second or fourth utterance</strong> is not socially acceptable, please modify it.</li>
                        <!-- <li><span class="badge badge-danger">New!</span> <u>If all of the utterances are already coherent</u>, -->
                        <li><span class="badge badge-danger">New!</span> <strong>change the first utterance to be diverse in structure!</strong> Use your creative thinking :)
                           <!-- <ul>
                              <li>
                                 For example, change "I'm going to throw my toy out the window" to <strong>"What do you think of throwing ~"</strong> or <strong>"How about I ~"</strong> or <strong>"I want to ~"</strong> or <strong>"Do I really have to ~?"</strong> or <strong>"Can I ~?"</strong>.</li>
                              </li>
                           </ul> -->
                        </li><li><span class="badge badge-danger">New!</span> modify the second utterance to be more colloquial by adding reactions or additional expressions.
                           <!-- like "Are you serious? Why would you~", "I hope you're joking, ~".</li> -->
                     </li></ul>
                     <!-- </p> -->
                     <div class="col-12 alert alert-danger" id="fix-length-warning" style="display: none;">You should change at least one of the utterances.</div>
                     <div class="col-12 alert alert-danger" id="fix-identity-warning" style="display: none;">You should modify the utterance not copy-paste it.</div>
                     <!-- <p class="card-text"> -->
                        <div class="form-group row"><textarea class="form-control" id="fix1" name="fix1" oninput="changeDialog(this);" placeholder="Modify: I poured the hot coffee on the customer" rows="2" style="width: 100%;"></textarea></div>
                        <div class="form-group row"><textarea class="form-control" id="fix2" name="fix2" oninput="changeDialog(this);" placeholder="Modify: Where were you when you did this? It doesn't sound like something you would do." rows="2" style="width: 100%;">I'm shocked you would do this. Why would you do this?</textarea></div>
                        <div class="form-group row"><textarea class="form-control" id="fix3" name="fix3" oninput="changeDialog(this);" placeholder="Modify: The customer made me mad." rows="2" style="width: 100%;"></textarea></div>
                        <div class="form-group row"><textarea class="form-control" id="fix4" name="fix4" oninput="changeDialog(this);" placeholder="Modify: It is not okay to pour coffee on someone on purpose.  It is especially not okay to do this at work." rows="4" style="width: 100%;"></textarea></div>
                        <div class="form-group row"><textarea class="form-control" id="fix5" name="fix5" oninput="changeDialog(this);" placeholder="Modify: The customer was an asshole, every day he complains about something." rows="2" style="width: 100%;"></textarea></div>
                     <p></p>
                  </div>
               </div>
            </div>
         </div>
         <div id="question" class="row mb-3 question-choice-container">
            <div class="col col-12 p-2 mb-2 text-white" style="background-color: #10a276"><span style="font-size:140%">Gently guide the other speaker to be more prosocial! <span class="emoji-bytes" data-emoji-bytes="[240, 159, 166, 140]">🦌</span><span class="emoji-bytes" data-emoji-bytes="[240, 159, 142, 132]">🎄</span></span></div>
            <p>
            </p><p class="text-body">Continue the dialogue by writing a response (1~3 sentences) which guides the speaker to be more prosocial based on the rule-of-thumb you choose.</p>
               <strong>If the speaker's behavior is <span class="badge badge-warning">problematic</span> (e.g., disturbing, unethical, rude, biased, dangerous) and:</strong>
               <ul>
                  <li>
                     if the other speaker <span class="badge badge-danger">rejects</span> the critique <strong>â guide the speaker to be more prosocial</strong> (as opposed to anti-social):
                     <ul>
                        <li><i><u>Some tips</u></i>:</li>
                        <li>Kindly suggest or wisely advise the speaker to do socially accepted behaviors</li>
                        <li>Let the speaker know about the better alternate results when doing socially accepted behaviors</li>
                        <li>The art of persuasion is in making the other also want what you want, not making them do what you want</li>
                     </ul>
                        â "<i>Don't you also want to have a happy relationship with your family? How about a nice dinner with your parent rather then shouting?</i>"
                  </li>
                  <li>
                     if the other speaker <span class="badge badge-primary">accepts</span> the critique and agrees to behave good <strong>â compliment their behavior :)</strong>
                     <ul>
                        <li><i><u>Some tips</u></i>:</li>
                        <li>Tell the speaker it was a good decision to make</li>
                        <li>Let them know it will lead to better results (e.g., friends or families will like it)</li>
                     </ul>
                  </li>
                     â "<i>I'm glad to hear that. I'm sure your friend will feel better regarding the accident.</i>"
               </ul>

               <span>If the speaker's behavior was <span class="badge badge-success">safe</span> in the first place and nothing is problematic at all <strong>â freely continue the dialogue in a gentle manner</strong></span>
               <ul>
                  <li>Ask questions or empathize or relate to your experience. </li>
               </ul>
            <p></p>

            <div class="card-group col-12">
               <div class="card">
                  <div class="card-body">
                    <h5 class="card-title">The conversation you modified</h5>
                    <p class="card-text">
                      </p><div class="imessage">
                        <p class="from-them"><span id="fix1-text-orig">I poured the hot coffee on the customer</span><span id="fix1-text" style="display:none;">fix</span></p>

                        <p class="from-me"><span id="fix2-text-orig" style="display: none;">Where were you when you did this? It doesn't sound like something you would do.</span><span id="fix2-text" style="">I'm shocked you would do this. Why would you do this?</span></p>

                        <p class="from-them"><span id="fix3-text-orig">The customer made me mad.</span><span id="fix3-text" style="display:none;">fix</span></p>

                        <p class="from-me"><span id="fix4-text-orig">It is not okay to pour coffee on someone on purpose.  It is especially not okay to do this at work.</span><span id="fix4-text" style="display:none;">fix</span></p>

                        <p class="from-them"><span id="fix5-text-orig">The customer was an asshole, every day he complains about something.</span><span id="fix5-text" style="display:none;">fix</span></p>

                        <p class="from-me"><span id="response-text-orig"></span><span id="response-text" style="display:none;">fix</span></p>
                      </div>
                    <p></p>
                    <!-- <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                    <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p> -->
                  </div>
                  <div class="card-footer">
                    <div class="form-group"><textarea class="form-control" id="response" name="response" oninput="updateCounter(this,1,3,30,400);changeDialog(this);" placeholder="Write your response here (> 30 characters)" required="" rows="5"></textarea><span id="response-sentence-counter">0 sentences (0 characters) detected</span></div>
                    <div class="col-12 alert alert-danger" id="response-length-warning" style="display: none;">Your response must be 30 ~ 500 characters (including spaces).</div>
                    <div class="col-12 alert alert-danger" id="sentence-count-warning" style="display: none;">Your response must be 1 ~ 3 sentences.</div>
                    <p class="text-primary"><small><i>Please be gentle and kind even if the other speaker is not.</i></small></p>
                  </div>
               </div>
               <div class="card">
                 <div class="card-body">
                   <!-- <h5 class="card-title">Write or select the rules-of-thumb (RoT) <br>implied in your response</h5> -->
                   <p class="card-text">
                     </p><ul>
                        <!-- <li><span class="badge badge-danger">New guideline </span>Regardless of the type of the speaker's response (accept/reject/etc), write or select the RoT which is implied in your response.</li> -->
                        <span class="badge badge-danger">New guideline</span> Regardless of the type of your response (e.g., suggestion, compliment, guidance), write or select the RoT implied in the response. Shortened examples below:
                        <!-- <span class="badge badge-danger">New guideline</span>  -->
                        <!-- <ul> -->
                           <li><strong>A:</strong> I think it was the right thing to do.<br><strong>B:</strong> It certainly is. I applaud you for being an involved citizen.<br><strong>RoT:</strong> It's good to exercise your civic duty <strong>(Previous RoT)</strong></li>
                           <li><strong>A:</strong> I don't feel well, I'd rather play video games at home.<br><strong>B:</strong> If you're sick and really feel uncomfortable going to the party then it's a good idea to stay home.<br><strong>RoT:</strong> You should attend big events of your friend (Previous RoT) â It's ok not to go to a party if you're sick <strong>(New RoT)</strong></li>

                        <!-- </ul> -->
                        <!-- <li>Please write a rule-of-thumb that you actually reflected in the response you wrote.</li> -->
                        <!-- <li><span class="badge badge-success">Note!</span> If nothing is problematic with the speaker, select the <b>[no RoT needed]</b> option. <u><i>This inlcudes</i></u>: </li>
                        <ul>
                           <li>the speaker willingly accepted the critique</li>
                           <li>The problematic issue in the dialogue is resolved</li>
                           <li>there was nothing socially problematic (unethical, rude, biased, disturbing, dangerous) in the dialogue at all</li>
                        </ul> -->
                     </ul>
                   <div class="imessage">
                        <div class="form-check">
                           <p class="from-social no-tail"><label class="btn form-check-label bg-transparent text-dark"><input class="form-check-input" id="s6" name="norm" type="radio" value="s6" required="">
                              <span><strong>A new rule-of-thumb is implied in my response</strong></span>
                           </label>
                           <textarea class="form-control" style="background-color:white" id="socialnew" name="socialnew" placeholder="Please write your rule-of-thumb here" rows="2"></textarea>
                        </p>
                        </div>
                        <div class="form-check">
                           <p class="from-social no-tail">
                              <label class="btn form-check-label bg-transparent text-dark text-left"><input class="form-check-input" id="s1" name="norm" type="radio" value="s1" required="" checked="">
                                 <span><strong>The previously chosen RoTs are implied in my response</strong></span><br>
                              </label>
                              <span>* You shouldn't spill coffee on people.</span><br><span>* [NONE]</span><br><span>* [NONE]</span><br><span>* [NONE]</span><br><span>* [NONE]</span>
                           </p>
                        </div>
                   </div>
                  <p></p>
                  <hr>
                     <p class="card-text">
                        <span class="badge badge-success">Note</span> If the previously selected RoT itself is somewhat problematic, please click the checkbox below and modify the RoT.
                        </p><div class="form-check">
                           <p class="no-tail">
                              <label class="btn form-check-label bg-transparent text-dark text-left"><input class="form-check-input" id="s7" name="norm_fix" type="checkbox" value="s7">
                                 <span><strong>The previous RoT is problematic, it should rather be:</strong></span><br>
                              </label>
                           <textarea class="form-control" style="background-color:white" id="socialfix" name="socialfix" placeholder="Please write the revised rule-of-thumb here. If there are multiple RoTs, seperate them with semicolons (;)" rows="2"></textarea>
                           </p>
                        </div>
                        <!-- <div class="form-check">
                          <p class="from-social no-tail"><label class="btn form-check-label bg-transparent text-dark"><input class="form-check-input" id="s2" name="norm" type="checkbox" value="s2" required/> <span class="statement">[NONE]</span></label></p>
                           <p class="from-social no-tail">
                              <label class="btn form-check-label bg-transparent text-dark text-left"><input class="form-check-input" id="s2" name="norm" type="radio" value="s2" required/>
                                 <strong>[No RoT needed] speaker's behavior is not problematic</strong>
                              </label>
                              <span>including: <br>* The speaker willingly accepted the critique</span>
                              <span><br>* The problematic issue in the dialogue is resolved</span>
                              <span><br>â Thus, no need for rules-of-thumb</span>
                           </p>
                        </div> -->
                     <p></p>
                 </div>
               </div>
             </div>
         </div>
         <!-- <div><p>We removed the attention check for you <span class='emoji-bytes' data-emoji-bytes='[240, 159, 152, 137]'></span></p></div> -->
         <div class="form-group">
            <div class="form-check"><input checked="checked" class="form-check-input" id="certify-no-pii-response" name="certify-no-pii-response" required="" type="checkbox"> <label class="form-check-label" for="certify-no-pii-response"> I certify that my response contains no personally identifiable information (name, address, SNN, etc) about me or anyone else.</label></div>
         </div>
         <!-- <input type='hidden' value='false' name='qtype' id='qtype'>
         <input type='hidden' value='false' name='pass' id='pass'> -->

         <!-- <div id="question" class="row mb-3 question-choice-container">
            <div class="col col-12 p-2 mb-2 text-white" style="background-color: #10a276"><span style="font-size:140%">Write a response to continue the conversation! <span class='emoji-bytes' data-emoji-bytes='[240, 159, 166, 140]'></span><span class='emoji-bytes' data-emoji-bytes='[240, 159, 142, 133]'></span><span class='emoji-bytes' data-emoji-bytes='[240, 159, 143, 187]'></span></span></div>
            <p class="text-body">What would you say in the given situation?</p>
            <ul>
            <div class="form-group"><textarea class="form-control" id="response" name="response" oninput="updateCounter(this,2,3,30,500);" placeholder="Write your response here (> 30 characters)" required="" rows="3"></textarea><span id="response-sentence-counter">0 sentences (0 characters) detected</span></div>
            <div class="col-12 alert alert-danger" id="response-length-warning" style="display: none;">Your response must be 20 ~ 500 characters (including spaces).</div>
            <div class="col-12 alert alert-danger" id="sentence-count-warning" style="display: none;">Your response must be 2 ~ 3 sentences.</div>
               <li>Continue the conversation you chose by writing a response which constructively critiques the unethical or rude behavior based on the rule-of-thumb you chose.</li>
            <li><span class="badge badge-danger">New!</span> <strong>We recommend you follow the DOs and DON'Ts below:</strong></li>
            <ul>
               <li>
                  <strong>DOs</strong>
                     <ul>
                        <li>Stay <strong>calm</strong> and maintain a <strong>positive tone</strong></li>
                        <li><strong>Label the comment</strong>, not the person. Example: "<em>Those words come from a racist stereotype.</em>"</li>
                        <li><strong>Respect cultural differences</strong></li>
                        <li><strong>Point out hasty generalization</strong></li>
                        <li><strong>Encourage putting oneself in other people's shoes</strong></li>
                        <li><span class="badge badge-success">Note!</span> <strong>Gently guide what the other should do instead to be socially acceptable</strong> (e.g., <em>learn about it by reading or watching useful resources</em>). This can help de-escalate the conflict. Example: "<em>I heard that there's a nice Netflix show about it. Why don't you give it a try to learn about them more?</em>"</li>
                        <li><strong>Refer to potential outcomes of such hate speech</strong> Example: "<em>That could hurt someone, You might be in a similar situation someday.</em>"</li>
                        <li><strong>Include context-specific information and rules-of-thumb</strong></li>
                        <li>Write about <span class="key-term">two ~ three</span> sentences. (four is also okay if it's not too long)</li>
                     </ul>
               </li>
               <li>
                  <strong>DON'Ts</strong>
                     <ul>
                        <li><strong>Don't label the speaker</strong> - for example, <em>calling them a bigot.</em></li>
                        <li><strong>Don't be hostile, insulting, or aggressive</strong>, it can escalate the conflict.</li>
                        <li><strong>Don't talk down to the speaker</strong></li>
                        <li><strong>Don't write responses that are too general</strong> - for example, "<em>Don't say that.</em>"</li>
                     </ul>
               </li>
            </ul>
            <li>If you want to learn more on how to give effective counterspeech, you can check out the <a href="https://dangerousspeech.org/wp-content/uploads/2016/10/Considerations-for-Successful-Counterspeech.pdf">https://dangerousspeech.org</a>! </li>
            <p><small><span style="color:#A52A2A;">We strongly discourage copying the rule-of-thumb as is. Try to blend the context-specific information with the rules-of-thumb.</span></small></p>
            <div class="form-group">
               <div class="form-check"><input checked="checked" class="form-check-input" id="certify-no-pii-response" name="certify-no-pii-response" required="" type="checkbox" /> <label class="form-check-label" for="certify-no-pii-response"> I certify that my response contains no personally identifiable information (name, address, SNN, etc) about me or anyone else.</label></div>
            </div>
         </div> -->

         <!-- OPTIONAL FEEDBACK -->
         <div class="row mt-5 mb-5">
            <div class="col-8 offset-2 col-lg-6 offset-lg-3">
               <p><span class="emoji-bytes" data-emoji-bytes="[240, 159, 148, 148]">🔔</span> <strong>Optional Feedback</strong>: Thanks for filling out the HIT above! If something about the HIT was unclear, please leave a comment in the box below! We would like to make this HIT easier for future workers, so we really appreciate feedback though it is optional. If you have concerns or questions, please email us!</p>
               <textarea id="feedback" name="feedback" rows="3"></textarea>
            </div>
         </div>
         <!-- SUBMIT BUTTON -->
         <div class="row mt-5">
            <div class="col-2 offset-5">
               <input class="btn btn-primary" id="submitButton" onclick="getnext()" type="submit" value="Submit">
            </div>
         </div>
         
         <script language="Javascript">turkSetAssignmentID();</script>
      </div>
      <!-- MTURK INPUT END -->
   </div></form>
   <!-- HIT END -->
   <!-- BOOSTRAP JS -->
   <!-- <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script> -->
   <script src="https://code.jquery.com/jquery-3.3.1.js" integrity="sha256-2Kok7MbOyxpgUVvAk/HJ2jigOSYS2auK4Pfzbm7uH60=" crossorigin="anonymous"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
   <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
   <!-- HITPUB JS -->
   <script id="hitpub_js">
      var e;
      var condition;
      $(document).ready(function() {
      var qtype = Math.floor(Math.random() * 3);
      $('#qtype').val(qtype)
      if(qtype == 0){
          $('.aq2').each(function(){$(this).hide();});
          $('.aq3').each(function(){$(this).hide();});
          $('.aq1').each(function(){$(this).show();});
      } else if(qtype == 1){
          $('.aq1').each(function(){$(this).hide();});
          $('.aq3').each(function(){$(this).hide();});
          $('.aq2').each(function(){$(this).show();});
      } else if(qtype == 2){
          $('.aq1').each(function(){$(this).hide();});
          $('.aq2').each(function(){$(this).hide();});
          $('.aq3').each(function(){$(this).show();});
      }
      $('.statement').each(function(){
          if($(this).text() === "[NONE]"){
              $(this).closest('div').hide();
          };
      });
      });

      (function () { var e, t; e = this, t = function () { var r = { startStopTimes: {}, idleTimeoutMs: 3e4, currentIdleTimeMs: 0, checkStateRateMs: 250, active: !1, idle: !1, currentPageName: "default-page-name", timeElapsedCallbacks: [], userLeftCallbacks: [], userReturnCallbacks: [], trackTimeOnElement: function (e) { var t = document.getElementById(e); t && (t.addEventListener("mouseover", function () { r.startTimer(e) }), t.addEventListener("mousemove", function () { r.startTimer(e) }), t.addEventListener("mouseleave", function () { r.stopTimer(e) }), t.addEventListener("keypress", function () { r.startTimer(e) }), t.addEventListener("focus", function () { r.startTimer(e) })) }, getTimeOnElementInSeconds: function (e) { var t = r.getTimeOnPageInSeconds(e); return t || 0 }, startTimer: function (e, t) { if (e || (e = r.currentPageName), void 0 === r.startStopTimes[e]) r.startStopTimes[e] = []; else { var n = r.startStopTimes[e], i = n[n.length - 1]; if (void 0 !== i && void 0 === i.stopTime) return } r.startStopTimes[e].push({ startTime: t || new Date, stopTime: void 0 }), r.active = !0, r.idle = !1 }, stopAllTimers: function () { for (var e = Object.keys(r.startStopTimes), t = 0; t < e.length; t++)r.stopTimer(e[t]) }, stopTimer: function (e, t) { e || (e = r.currentPageName); var n = r.startStopTimes[e]; void 0 !== n && 0 !== n.length && (void 0 === n[n.length - 1].stopTime && (n[n.length - 1].stopTime = t || new Date), r.active = !1) }, getTimeOnCurrentPageInSeconds: function () { return r.getTimeOnPageInSeconds(r.currentPageName) }, getTimeOnPageInSeconds: function (e) { var t = r.getTimeOnPageInMilliseconds(e); return void 0 === t ? void 0 : t / 1e3 }, getTimeOnCurrentPageInMilliseconds: function () { return r.getTimeOnPageInMilliseconds(r.currentPageName) }, getTimeOnPageInMilliseconds: function (e) { var t = r.startStopTimes[e]; if (void 0 !== t) { for (var n = 0, i = 0; i < t.length; i++) { var s = t[i].startTime, o = t[i].stopTime; void 0 === o && (o = new Date), n += o - s } return Number(n) } }, getTimeOnAllPagesInSeconds: function () { for (var e = [], t = Object.keys(r.startStopTimes), n = 0; n < t.length; n++) { var i = t[n], s = r.getTimeOnPageInSeconds(i); e.push({ pageName: i, timeOnPage: s }) } return e }, setIdleDurationInSeconds: function (e) { var t = parseFloat(e); if (!1 !== isNaN(t)) throw { name: "InvalidDurationException", message: "An invalid duration time (" + e + ") was provided." }; return r.idleTimeoutMs = 1e3 * e, this }, setCurrentPageName: function (e) { return r.currentPageName = e, this }, resetRecordedPageTime: function (e) { delete r.startStopTimes[e] }, resetAllRecordedPageTimes: function () { for (var e = Object.keys(r.startStopTimes), t = 0; t < e.length; t++)r.resetRecordedPageTime(e[t]) }, resetIdleCountdown: function () { r.idle && r.triggerUserHasReturned(), r.idle = !1, r.currentIdleTimeMs = 0 }, callWhenUserLeaves: function (e, t) { this.userLeftCallbacks.push({ callback: e, numberOfTimesToInvoke: t }) }, callWhenUserReturns: function (e, t) { this.userReturnCallbacks.push({ callback: e, numberOfTimesToInvoke: t }) }, triggerUserHasReturned: function () { if (!r.active) for (var e = 0; e < this.userReturnCallbacks.length; e++) { var t = this.userReturnCallbacks[e], n = t.numberOfTimesToInvoke; (isNaN(n) || void 0 === n || 0 < n) && (t.numberOfTimesToInvoke -= 1, t.callback()) } r.startTimer() }, triggerUserHasLeftPage: function () { if (r.active) for (var e = 0; e < this.userLeftCallbacks.length; e++) { var t = this.userLeftCallbacks[e], n = t.numberOfTimesToInvoke; (isNaN(n) || void 0 === n || 0 < n) && (t.numberOfTimesToInvoke -= 1, t.callback()) } r.stopAllTimers() }, callAfterTimeElapsedInSeconds: function (e, t) { r.timeElapsedCallbacks.push({ timeInSeconds: e, callback: t, pending: !0 }) }, checkState: function () { for (var e = 0; e < r.timeElapsedCallbacks.length; e++)r.timeElapsedCallbacks[e].pending && r.getTimeOnCurrentPageInSeconds() > r.timeElapsedCallbacks[e].timeInSeconds && (r.timeElapsedCallbacks[e].callback(), r.timeElapsedCallbacks[e].pending = !1); !1 === r.idle && r.currentIdleTimeMs > r.idleTimeoutMs ? (r.idle = !0, r.triggerUserHasLeftPage()) : r.currentIdleTimeMs += r.checkStateRateMs }, visibilityChangeEventName: void 0, hiddenPropName: void 0, listenForVisibilityEvents: function () { void 0 !== document.hidden ? (r.hiddenPropName = "hidden", r.visibilityChangeEventName = "visibilitychange") : void 0 !== document.mozHidden ? (r.hiddenPropName = "mozHidden", r.visibilityChangeEventName = "mozvisibilitychange") : void 0 !== document.msHidden ? (r.hiddenPropName = "msHidden", r.visibilityChangeEventName = "msvisibilitychange") : void 0 !== document.webkitHidden && (r.hiddenPropName = "webkitHidden", r.visibilityChangeEventName = "webkitvisibilitychange"), document.addEventListener(r.visibilityChangeEventName, function () { document[r.hiddenPropName] ? r.triggerUserHasLeftPage() : r.triggerUserHasReturned() }, !1), window.addEventListener("blur", function () { r.triggerUserHasLeftPage() }), window.addEventListener("focus", function () { r.triggerUserHasReturned() }), document.addEventListener("mousemove", function () { r.resetIdleCountdown() }), document.addEventListener("keyup", function () { r.resetIdleCountdown() }), document.addEventListener("touchstart", function () { r.resetIdleCountdown() }), window.addEventListener("scroll", function () { r.resetIdleCountdown() }), setInterval(function () { r.checkState() }, r.checkStateRateMs) }, websocket: void 0, websocketHost: void 0, setUpWebsocket: function (e) { if (window.WebSocket && e) { var t = e.websocketHost; try { r.websocket = new WebSocket(t), window.onbeforeunload = function () { r.sendCurrentTime(e.appId) }, r.websocket.onopen = function () { r.sendInitWsRequest(e.appId) }, r.websocket.onerror = function (e) { console && console.log("Error occurred in websocket connection: " + e) }, r.websocket.onmessage = function (e) { console && console.log(e.data) } } catch (e) { console && console.error("Failed to connect to websocket host.  Error:" + e) } } return this }, websocketSend: function (e) { r.websocket.send(JSON.stringify(e)) }, sendCurrentTime: function (e) { var t = { type: "INSERT_TIME", appId: e, timeOnPageMs: r.getTimeOnCurrentPageInMilliseconds(), pageName: r.currentPageName }; r.websocketSend(t) }, sendInitWsRequest: function (e) { var t = { type: "INIT", appId: e }; r.websocketSend(t) }, initialize: function (e) { var t = r.idleTimeoutMs || 30, n = r.currentPageName || "default-page-name", i = void 0, s = void 0; e && (t = e.idleTimeoutInSeconds || t, n = e.currentPageName || n, i = e.websocketOptions, s = e.initialStartTime), r.setIdleDurationInSeconds(t).setCurrentPageName(n).setUpWebsocket(i).listenForVisibilityEvents(), r.startTimer(void 0, s) } }; return r }, "undefined" != typeof module && module.exports ? module.exports = t() : "function" == typeof define && define.amd ? define([], function () { return e.TimeMe = t() }) : e.TimeMe = t() }).call(this);

      TimeMe.initialize({
          currentPageName: "task",
          idleTimeoutInSeconds: 30
      });

      $(document).ready(function() {
          $('#submitButton').click(function () {
              try {
                  $('input[name=ee]').attr('value', TimeMe.getTimeOnCurrentPageInSeconds());
              } catch {
              }
              return true;
          });
      });

      $(document).ready(function() {
         $('span.emoji-bytes').each(displayEmoji);
      });

      function toggleConsent(checked){
        if (checked){
          $("#main-task").show();
          $("#consent-message").hide();
        } else {
          $("#main-task").hide();
          $("#consent-message").show();
        }
      }

      function attentionCheck(radio) {
        var qtype = $('#qtype').val()
        if (qtype == 0 && radio.checked && radio.id == "attention4") {
          $('#pass').val('true')
        } else if (qtype == 1 && radio.checked && radio.id == "attention3") {
          $('#pass').val('true')
        } else if (qtype == 2 && radio.checked && radio.id == "attention2") {
          $('#pass').val('true')
        } else {
          $('#pass').val('false')
        }
      }

      function changeText(radio) {
        if (radio.checked && radio.id == "d1") {
          $('.fix1-text').each(function(){$(this).show();});
          $('.fix2-text').each(function(){$(this).hide();});
          $('.fix3-text').each(function(){$(this).hide();});
          $('.fix4-text').each(function(){$(this).hide();});
          $('.fix5-text').each(function(){$(this).hide();});
        } else if (radio.checked && radio.id == "d2") {
          $('.fix1-text').each(function(){$(this).hide();});
          $('.fix2-text').each(function(){$(this).show();});
          $('.fix3-text').each(function(){$(this).hide();});
          $('.fix4-text').each(function(){$(this).hide();});
          $('.fix5-text').each(function(){$(this).hide();});
        } else if (radio.checked && radio.id == "d3") {
          $('.fix1-text').each(function(){$(this).hide();});
          $('.fix2-text').each(function(){$(this).hide();});
          $('.fix3-text').each(function(){$(this).show();});
          $('.fix4-text').each(function(){$(this).hide();});
          $('.fix5-text').each(function(){$(this).hide();});
        }
      }
      function changeDialog(el) {
        var name = el.id;
        var text = $(el).prop("value");
        var fixed_utterance = $("#"+name+"-text");
        var original_utterance = $("#"+name+"-text-orig");
        if (text.length > 0){
          document.getElementById(name+"-text").textContent = text;
          fixed_utterance.show();
          original_utterance.hide();
        } else {
          fixed_utterance.hide();
          original_utterance.show();
        }
      }

      $(function(){
          var requiredCheckboxes = $('.imessage :checkbox[required]');
          requiredCheckboxes.change(function(){
              if(requiredCheckboxes.is(':checked')) {
                  requiredCheckboxes.removeAttr('required');
              } else {
                  requiredCheckboxes.attr('required', 'required');
              }
          });
      });

      function countSentences(text){
        var match = text.match(/[\w\)"][.?!](?:\s|$)/gm);
        return match === null ? 0: match.length;
      }
      function updateCounter(el,minS,maxS,minC,maxC){
        var name = el.id;
        var counter = $("#"+name+"-sentence-counter");
        var text = $(el).prop("value");
        var nSents = countSentences(text);
        var nChars = text.length;
        var warnText = "";
        counter.css('color', 'black');

        if (nSents >= minS && nChars < maxC)
          warnText = " â";

        if (nSents > maxS || nChars > maxC) {
          warnText = " (try shortening it)";
          counter.css('color', '#721c24');
        }
        counter.html(nSents+" sentences ("+nChars+" characters) detected"+warnText);
      }

      function checkResponse(){
        var response = $("#response").prop("value");
      //   var fixed_utterance = $("#"+name+"-sentence-counter");
        var fixed_utterance1 = $("#fix1").prop("value");
        var fixed_utterance2 = $("#fix2").prop("value");
        var fixed_utterance3 = $("#fix3").prop("value");
        var fixed_utterance4 = $("#fix4").prop("value");
        var fixed_utterance5 = $("#fix5").prop("value");

        var original_utterance1 = $("#context1").text();
        var original_utterance2 = $("#context2").text();
        var original_utterance3 = $("#context3").text();
        var original_utterance4 = $("#context4").text();
        var original_utterance5 = $("#context5").text();

        var nSents = countSentences(response);
        if (response.length > 20 && response.length < 500){
          $("#response").attr("data-state","open");
          $("#response-length-warning").hide();
          if (nSents >= 1 && nSents < 4){
            $("#sentence-count-warning").hide();
            if (fixed_utterance1.length > 0 || fixed_utterance2.length > 0 || fixed_utterance3.length > 0 || fixed_utterance4.length > 0 || fixed_utterance5.length > 0){
               if (fixed_utterance1 === original_utterance1 || fixed_utterance2 === original_utterance2 || fixed_utterance3 === original_utterance3 || fixed_utterance4 === original_utterance4 || fixed_utterance5 === original_utterance5) {
                  $("#fix-identity-warning").show();
                  return false;
               } else {
                  return true;
               }
            } else {
              $("#fix-length-warning").show();
              return false;
            }
          }
          $("#sentence-count-warning").show();
          return false;
        } else {
          $("#response").attr("data-state","invalid");
          $("#response-length-warning").show();
          return false;
        }
      }
      $("#submitButton").on("click",function(e){
        var ok = checkResponse();
        console.log("Answer ok? "+ok);

        if (!ok) {
          $("#cantSubmit").show();
          $(":invalid").addClass("invalid");
          $(".lickert>input:invalid").parents().addClass("invalid");
          $(".form-check>input:invalid").parents().addClass("invalid");
          e.preventDefault();
        } else{
          $("#cantSubmit").hide();
          return true;
        }
      });
   </script>

   <script id="emoji_js">
      function displayEmoji() {

      /**
       * utf8ByteArrayToString() copied from:
       *   https://github.com/google/closure-library/blob/e877b1eac410c0d842bcda118689759512e0e26f/closure/goog/crypt/crypt.js
       *
       * Converts a UTF-8 byte array to JavaScript's 16-bit Unicode.
       * @param {Uint8Array|Array<number>} bytes UTF-8 byte array.
       * @return {string} 16-bit Unicode string.
       */
      var utf8ByteArrayToString = function(bytes) {
      var out = [], pos = 0, c = 0;
      while (pos < bytes.length) {
         var c1 = bytes[pos++];
         if (c1 < 128) {
            out[c++] = String.fromCharCode(c1);
         } else if (c1 > 191 && c1 < 224) {
            var c2 = bytes[pos++];
            out[c++] = String.fromCharCode((c1 & 31) << 6 | c2 & 63);
         } else if (c1 > 239 && c1 < 365) {
            // Surrogate Pair
            var c2 = bytes[pos++];
            var c3 = bytes[pos++];
            var c4 = bytes[pos++];
            var u = ((c1 & 7) << 18 | (c2 & 63) << 12 | (c3 & 63) << 6 | c4 & 63) -
                  0x10000;
            out[c++] = String.fromCharCode(0xD800 + (u >> 10));
            out[c++] = String.fromCharCode(0xDC00 + (u & 1023));
         } else {
            var c2 = bytes[pos++];
            var c3 = bytes[pos++];
            out[c++] =
            String.fromCharCode((c1 & 15) << 12 | (c2 & 63) << 6 | c3 & 63);
         }
      }
      return out.join('');
      }

      jQuery(this).text(utf8ByteArrayToString(JSON.parse(jQuery(this).attr('data-emoji-bytes'))));
      }
   </script>
   <!-- For charting JS -->
   <script src="https://cdn.anychart.com/releases/8.9.0/js/anychart-base.min.js" type="text/javascript"></script>
   <!-- LIGHTBOX JS -->
   <script src="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.1/js/lightbox-plus-jquery.min.js"></script>

      
    
  

<div id="lightboxOverlay" tabindex="-1" class="lightboxOverlay" style="display: none;"></div><div id="lightbox" tabindex="-1" class="lightbox" style="display: none;"><div class="lb-outerContainer"><div class="lb-container"><img class="lb-image" src="data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" alt=""><div class="lb-nav"><a class="lb-prev" aria-label="Previous image" href=""></a><a class="lb-next" aria-label="Next image" href=""></a></div><div class="lb-loader"><a class="lb-cancel"></a></div></div></div><div class="lb-dataContainer"><div class="lb-data"><div class="lb-details"><span class="lb-caption"></span><span class="lb-number"></span></div><div class="lb-closeContainer"><a class="lb-close"></a></div></div></div></div></body></html>
""",
  os.path.join("img", "ex9.png"),
"self.actions.modify_radio('norm', 's1')"
  ]

  return [instance_1, instance_2, instance_3, instance_4, instance_5, instance_6, instance_7, instance_8, instance_9]

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