import React from 'react';
import PieModule from './pieModule';
import {Button, ButtonToolbar} from 'react-bootstrap';
import SurveyClient from './SurveyClient';

class App extends React.Component {

    constructor(properties){
        const data = [{
            id: '02b8ed4f-8be6-4753-83ee-4d708a1f74a8',
            text: "",
            data: [
            {label: "Positive", value: 70, color: "#009900"},
            {label: "Negative", value: 20, color: "#dd4b39"},
            {label: "Neutral", value: 10, color: "#3b5998"}]}];
        super(properties);
        this.state = {questions: data, secondsElapsed: 0};
        this.onButtonClick = this.onButtonClick.bind(this);
    }

    // componentDidMount() {
    //     // this.interval = setInterval(this.tick.bind(this), 10000);
    // }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    tick() {
        this.setState({questions: this.state.questions, secondsElapsed: this.state.secondsElapsed + 1});
    }

    getPieMarkup() {
        let pies = [];
        for (let question of this.state.questions){
            if(question.length !== 0) {
                pies.push(<div className="col-sm-4" style={{marginBottom: '25px'}}>
                            <p className="text-center">{question.text}</p>
                            <PieModule key={question.id} data={question.data} />
                          </div>)
            }
        }
        return pies;
    }

    onButtonClick(event) {
        const surveyClient = new SurveyClient("0000ed4f-8be6-4753-83ee-4d708a1f74a8");
        surveyClient.getSurveyResponse().then((response) => {
            return response.json();
        }).then((response) => {
            let questionArr = [];
            response.questions.forEach((question) => {
                let item = [];
                let total = Number(question.total), negative = Number(question.negative),
                    positive = Number(question.positive), neutral = Number(question.neutral);
                if(positive != 0){
                    item.push({label:"Positive", value: ((positive/total)*100), color: "#009900"});
                }
                if(negative != 0) {
                    item.push({label: "Negative", value: ((negative / total) * 100), color: "#dd4b39"});
                }
                if(neutral != 0) {
                    item.push({label: "Neutral", value: ((neutral / total) * 100), color: "#3b5998"});
                }
                questionArr.push({id: question.id, text: question.qstnTxt, data: item});
            });
            console.log(response);
            this.setState({questions: questionArr, secondsElapsed: this.state.secondsElapsed});
        });
    }

    render() {
        // this.onButtonClick();
        return (
            <div className="container" >
                <div className="row">
                    <h2>Sentiment Analysis of Responses</h2>
                    <div className="text-right">
                        <Button bsStyle="success" onClick={this.onButtonClick.bind()}>Refresh</Button>
                    </div>
                </div>
                <div className="row">
                    {
                        this.getPieMarkup()
                    }
                </div>
            </div>

        );
    }
}

export default App;