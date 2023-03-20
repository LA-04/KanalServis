import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import React from 'react';
import Chart from 'chart.js/auto';



class App extends React.Component{
    state = { details: [], }

    componentDidMount() {
        let data;
        axios.get('http://localhost:8000')
        .then(res => {
            const data = res.data;
            this.setState({ details: data }, () => {
                this.createChart();
            });
        })
        .catch(err => {
            console.log(err);
        });
}
    createChart = () => {
    const labels = this.state.details.map(detail => detail.ord_date);
    const prices = this.state.details.map(detail => detail.price_usd);

    const ctx = document.getElementById('myChart').getContext('2d');

    if (this.myChart) {
        this.myChart.destroy();
    }

    this.myChart = new Chart(ctx, {
      type: 'line',

      data: {
        labels: labels,
        datasets: [{
          label: 'Orders',
          data: prices,
          backgroundColor: 'rgb(41, 98, 163)',
          borderColor: 'rgb(41, 98, 163)',
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
    });
}
    render() {

        const totalUsd = this.state.details.reduce((acc, cur) => acc + cur.price_usd, 0);

        return (
        <div>
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous"/>
                <title>Hello, modularity!</title>
            </head>
            <body>
                <div>
                    <nav class="navbar" style={{backgroundColor: '#e3f2fd'}}>
                      <div class="container">
                        <a class="navbar-brand" href="#">
                          <img src="../logo.png" alt="Каналсервис" width="273" height="63"/>
                        </a>
                      </div>
                    </nav>
                    <div class="container mt-3">
                        <div class="row">
                            <div class="col d-flex justify-content-center align-items-center">
                                <canvas id="myChart"></canvas>
                            </div>
                            <div class="col justify-content-center">
                                <div class="w-50 mx-auto">
                                    <div class="card text-center">
                                      <div class="card-header">
                                        Total
                                      </div>
                                      <div class="card-body">
                                        <h2 class="card-title">{totalUsd}</h2>
                                      </div>
                                    </div>
                                </div>
                                <div class="overflow-auto mt-1" style={{height: '500px'}}>
                                    <table class="table">
                                      <thead>
                                        <tr>
                                          <th scope="col">№</th>
                                          <th scope="col">заказ №</th>
                                          <th scope="col">стоимость, $</th>
                                          <th scope="col">стоимость, Руб</th>
                                          <th scope="col">срок поставки</th>
                                        </tr>
                                      </thead>
                                      <tbody class="table-group-divider">
                                      {this.state.details.map((output, id) => (
                                        <tr key={id}>
                                          <th scope="row">{output.number}</th>
                                          <td>{output.order}</td>
                                          <td>{output.price_usd}</td>
                                          <td>{output.price_rub}</td>
                                          <td>{output.ord_date}</td>
                                        </tr>))}
                                      </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        </div>
        )
    }
}

export default App;
