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

  os.path.join("img", "ex4.png"),
  return [instance_1, instance_2, instance_3, instance_4]

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