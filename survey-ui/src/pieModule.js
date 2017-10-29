import React from "react"
import PieChart from "react-svg-piechart"

export default class PieModule extends React.Component {
    constructor() {
        super();

        this.state = {
            expandedSector: null,
        };

        this.handleMouseEnterOnSector = this.handleMouseEnterOnSector.bind(this)
    }

    handleMouseEnterOnSector(sector) {
        this.setState({expandedSector: sector})
    }

    render() {

        const {expandedSector} = this.state;
        return (
            <div className="container">
                <div className="row">
                    <div className="col-sm-3">
                        <PieChart
                            data={ this.props.data }
                            expandedSector={expandedSector}
                            onSectorHover={this.handleMouseEnterOnSector}
                            sectorStrokeWidth={2}
                            expandOnHover
                            shrinkOnTouchEnd
                        />
                        <div className="text-center">
                            {
                                this.props.data.map((element, i) => (
                                    <div key={i}>
                                        <span style={{background: element.color}}></span>
                                        <span style={{fontWeight: this.state.expandedSector === i ? "bold" : null}}>
                                {element.label} : {element.value.toFixed(2)} %
                            </span>
                                    </div>
                                ))
                            }
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}