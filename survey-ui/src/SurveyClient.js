import 'whatwg-fetch';

const HTTP_METHOD = {
    GET: 'GET'
};

export default class SurveyClient {
    constructor(surveyId) {
        this.surveyId = surveyId;
        this.surveyPath = `/surveyresponse/${this.surveyId}`;
    }

    getSurveyResponse() {
        return fetch(this.surveyPath);
    }
}