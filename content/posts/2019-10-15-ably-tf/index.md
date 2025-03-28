---
layout: posts
title: "Build a Traffic Alert App with just one html — Ably + Tensorflow"
date: 2019-10-15
description: "In this blog posts, we will showcase the power of Ably and Tensorflow.js. Everything will be just on the frontend, in just one html. It’s a demo, in production you may not do things this way but you can have a feeling how powerful Ably is and how you can use deep learning model with just a few lines of code."
image: /assets/images/scott-webb-hDyO6rr3kqk-unsplash.jpg
author: Cheuk Ting Ho
tags:
  - JavaScript
  - Web
---
In this blog post, we will showcase the power of Ably and Tensorflow.js. Everything will be just on the frontend, in just one html. It’s a demo, in production you may not do things this way but you can have a feeling how powerful Ably is and how you can use deep learning model with just a few lines of code.

## What is Ably?

Ably provide API to handle a lot of realtime Pub/Sub easily. In Ably, you can choose from Realtime, REST, MQTT or SSE library which is implemented in most of the popular languages and framework. For further information regarding Ably, you can visit their [webpage](https://www.ably.io/).
If you want to follow this demo and build your own, you have to sign up for a free Ably account and get an API key [here](https://www.ably.io/signup#signup-box).

## Let’s get started!

First, we will need all the basic components in an html. We will start with this file as a skeleton:

```html
<html>
  <body>
    <h1>TfL traffic notifier</h1>
    <p></p>
<div>
    Your update: <input type="text" id="message-text" value=""> <button id="send-message">Submit an update</button>
    </div>
    <textarea id="result" rows="10" style="width: 60%; margin-top: 10px; font-family: courier, courier new; background-color: #333; color: orange" disabled=""></textarea>
    </div>
  </body>
</html>
```

It’s very simple and basic. We are more interested in the functionality but not the graphical design. We have an input field for the user's input and a button to submit an update. The black text area underneath is for the messages from all users.

![demo picture 1](https://miro.medium.com/max/3116/1*bpFWHmn5sm8TgcnHeS11qA.png)

## Using Ably Realtime

We will use Ably Realtime WebSocket connection to publish and subscribe to a channel for the updated form users. (Make sure you have the API key) Put this after the `</body>` and before `</html>` :

```html
<!-- Include the latest Ably Library  -->
  <script src="https://cdn.ably.io/lib/ably.min-1.js"></script>
<!-- Instance the Ably library  -->
  <script type="text/javascript">
// Set up Ably's channel
    var realtime = new Ably.Realtime(<your API key>; // put your API key here
    var channel = realtime.channels.get("my_channel");
// Helper function for getting the timestamp
    function get_current_time(){
        return '[' + Date().toLocaleString() + ']\n';
    }
// Getting the update from users
    channel.subscribe(function(msg) {
        document.getElementById("result").innerHTML = (get_current_time() + "User update: " + msg.data + "\n\n") + document.getElementById("result").innerHTML;
    });
    document.getElementById("send-message").addEventListener("click", function(){
        let input_text = document.getElementById("message-text").value;
        if (input_text != ""){
                        channel.publish("update", input_text);
                        document.getElementById("message-text").value = ""
}
    })
  </script>
```

Here we:
1. Include the Ably library
2. Connect to Ably (remember to replace with your API
3. Subscribe to my_channel and if there is update, add it to the text
4. When the user inputs an update and clicks the button it will publish to my_channel

Now, try our app. Put something at the input box and click the button.

![demo picture 2](https://miro.medium.com/max/3092/1*O8fcVtPvA-Na1VjfW8fPlA.png)

You can see the update appear, you can also do an experiment for multiple users. Open the html files in another window or tab and repeat publish an update. You can see the ‘other user’ will also receive the update.
I would also like to point out that, using an API key like what we did is not a good practice in production code as it will expose your key to the public. To further understand how to do it properly, please refer to [Ably’s documentation](https://www.ably.io/documentation/core-features/authentication#token-authentication).

## TfL information — Ably Hub

Now we will be adding the TfL updates. Ably Hub which provides free, open-source data streaming for anyone to use (difference licence restriction may apply to different data source). If you have a source to donate, please get in touch with Ably’s team.

Using Ably Hub is very similar to using Ably Realtime, you can also refer to [this page](https://www.ably.io/hub/products/10#documentation) for the documentation specific to TfL data. Adding a new channel:

```js
var tfl_channel = realtime.channels.get("[product:ably-tfl/tube]tube:disruptions");
```

This will update us when we have disruptions on any lines. If there is not, we will get an empty list. We can then check our update to see does it contains information about disrupted lines:

```js
// Getting the update form TfL streamer
    tfl_channel.subscribe(function(msg) {
        if (msg.data.length == 0) {
            document.getElementById("result").innerHTML = (get_current_time() + "TfL: Good service on all lines." + "\n\n") + document.getElementById("result").innerHTML;
        }else{
            msg.data.forEach(function(each_issue){
                document.getElementById("result").innerHTML = (get_current_time() + each_issue.description + "\n\n") + document.getElementById("result").innerHTML;
            })
        }
    });
```

![demo picture 3](https://miro.medium.com/max/3080/1*-JnCNfhBhI4SUTkO3RA1CQ.png)

## Toxic detector — Tensorflow.js

So far all users can update no matter what they say, which is bad. Can we stop people publish toxic updates to our channel? Let’s try using AI and detect toxic comments and block them. Here we will use a pre-trained model and it is super easy, just add Tensorflow.js and the model:

```html
<!-- Include tf model -->
  <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
  <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/toxicity"></script>
```

And update the publish function:

```js
// When the user send an update, check if it is a toxic comment, publish if it is not.
    document.getElementById("send-message").addEventListener("click", function(){
        let input_text = document.getElementById("message-text").value;
        let threshold = 0.9;
        var all_prediction = false;
        if (input_text != ""){
            toxicity.load(threshold).then(function(model){
                model.classify(input_text).then(function(predictions){
                    predictions.forEach(function(each_prediction){
                        let results = each_prediction.results
                        if (results[0].match){
                            all_prediction = true;
                            return 0;
                        }
                    });
                    if (all_prediction){
                        alert("Please be nice.")
                    }else{
                        channel.publish("update", input_text);
                        document.getElementById("message-text").value = ""
                    }
                });
            });
        }
    })
```

Here we set a threshold of 0.9 so if our model is very confident that it contains toxic text in any form, it will prevent publishing instead it will remind the user to be nice.

![demo picture 4](https://miro.medium.com/max/3288/1*Yn1jkV6_tRlTa5Xm5kLOvw.png)

Trying it out, you will see that the speed of our message reduces significantly. Ably is a fast API as it uses WebSocket and the update in almost instant. However, making a prediction via the AI model takes a bit of time and is not ideal in terms of performance. Maybe we should not do everything at the frontend!

I hope you had fun! To see the finished html file as a whole, please refer to [the file](https://github.com/Cheukting/ably-tensorflow-demo/blob/master/ably%2Btensorflow_example.html) on GitHub
