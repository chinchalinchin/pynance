import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { Component, Input, OnInit } from '@angular/core';
import { Holding } from 'src/app/models/holding';
import { LogService } from 'src/app/services/log.service';
import { PynanceService } from 'src/app/services/pynance.service';
import { containsObject } from 'src/utilities';
import { DomSanitizer } from '@angular/platform-browser';


@Component({
  selector: 'app-risk-profile',
  templateUrl: './risk-profile.component.html'
})
export class RiskProfileComponent implements OnInit {
  private location : string = "app.widgets.risk-profile.RiskProfileComponent"
  public portfolio : Holding[] = [];
  public calculateDisabled :boolean = true;
  public clearDisabled : boolean = true;
  public loaded : boolean = false;
  public loading : boolean = false;
  public startDate : string = null;
  public endDate : string = null;
  public img: any = null

  @Input() 
  public explanationDisabled;
  
  constructor(private pynance : PynanceService,
              private sanitizer : DomSanitizer,
              private logs : LogService) { }

  ngOnInit(): void {
  }
  
  public calculate() : void{
    this.calculateDisabled = true;
    this.clearDisabled = false;
    this.loading = true;
    this.pynance.riskProfileJPEG(this.getTickers(), this.getEndDate(), this.getStartDate())
                  .subscribe( (imgData) =>{
                    let imgUrl = URL.createObjectURL(imgData)
                    this.img = this.sanitizer.bypassSecurityTrustUrl(imgUrl);
                    this.loaded = true;
                    this.loading = false;
                  })

  }

  public clear() : void {
    this.calculateDisabled = true;
    this.clearDisabled = true;
    this.loaded = false;
    this.loading = false;
    this.img = null;
  }

  public getTickers() : string[]{
    let tickers : string [] = []
    for(let holding of this.portfolio){
      tickers.push(holding.ticker)
    }
    return tickers;
  }

  public setTickers(inputTickers : string[]){
    this.logs.log(`received tickers: ${inputTickers}`, this.location)

    let unduplicatedTickers : string[] = [];
    let portfolioTickers : string[] = this.getTickers();
    
    for(let ticker of inputTickers){
      if(!containsObject(ticker, portfolioTickers)){ unduplicatedTickers.push(ticker); }
    }

    for(let ticker of unduplicatedTickers){
      this.portfolio.push({ ticker: ticker, allocation: null, shares: null, annual_return: null, annual_volatility: null})
    }

    this.calculateDisabled = false;
    this.clearDisabled = false;
  }

  public setDates(inputDates: string[]) : void {
    this.logs.log(`Received dates ${inputDates}`, this.location)
    this.startDate = inputDates[0]
    this.endDate = inputDates[1]
  }

  public getStartDate() : string { return this.startDate; }

  public getEndDate() : string { return this.endDate; }
}