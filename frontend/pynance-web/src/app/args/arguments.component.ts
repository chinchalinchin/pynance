import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { dateToString } from 'src/utilities';

/** ArgumentsComponent
 * DESCRIPTION: 
 * This component is used to parse user input and send it back to the parent 
 *  component in which it is placed. 
 * 
 * INPUT:
 * The ArgumentsComponent has five tags that must be specified as arguments when laying down 
 *  an instance of this component,
 * 
 *  <app-args [tickers]="true" [dates]="true" [target]="true" 
 *            [model]="true" [investment]="true" [method]="true"></app-args>
 * 
 * If these arguments are not provided, they default to false. These arguments configure
 *  which widgets are displayed in the component. If 'tickers' is specified, a text area will
 *  allow users to enter a list of ticker symbols separated by a comma. If 'dates' is specified,
 *  a date picker toggle will allow users to select a start date and end date. If 'target' is
 *  specified a number input field will allow users to enter a decimal. If 'model' is specified,
 *  a drop-down menu will be displayed which will allow users to select from the available pricing
 *  models (Discount Dividend Model, Discount Cashflow Model, etc.)
 * 
 * OUTPUT:
 * The ArgumentsComponent has four output events into which the parent component can wire in 
 *  functions,
 * 
 * <app-args (addTickers)="doThis($event)" (addDates)="doThat($event)" 
 *           (addTarget)="doSomething($event)" (addModel)="doAnything($event)"></app-args>
 * 
 * The 'addTickers' event will contain a string array of ticker symbol list inputted by the user. 
 *  Note, duplicate ticker symbols may exist in this list, so the parent component will have to 
 *  validate the list on its own. 
 * 
 * The 'addDates' event will contain a string array with the start and end date. 
 * 
 * TODOS
 * method: maximize sharpe or minimize volatilty
 **  */
@Component({
  selector: 'app-args',
  templateUrl: './arguments.component.html'
})
export class ArgumentsComponent implements OnInit {
  // Input: Displayed argument subcomponents
  @Input()
  private tickers : boolean = false;
  @Input()
  private dates : boolean = false;
  @Input()
  private target : boolean = false;
  @Input()
  private model: boolean = false;
  @Input()
  private investment: boolean = false;

  // Output: User entered argument values
  @Output()
  private addTickers = new EventEmitter<string[]>();
  @Output()
  private addDates = new EventEmitter<string[]>();
  @Output()
  private addTarget = new EventEmitter<number>();
  @Output()
  private addModel = new EventEmitter<string>();
  @Output()
  private addInvestment = new EventEmitter<number>();
  
  public inputTickers: string;
  public inputInvestment: number;
  public inputTarget: number;
  public range = new FormGroup({
    start: new FormControl(),
    end: new FormControl()
  });


  private savedTickers : string[] = [];
  private savedStartDate : Date;
  private savedEndDate : Date;
  private today : Date;

  constructor() { }

  ngOnInit() {
    this.today = new Date();
  }

  public setStartDate(date) : void {
    this.savedStartDate = date.value;
  }

  public setEndDate(date) : void {
    this.savedEndDate = date.value;
  }

  public saveTickers(){
    let parsedTickers : string[] = this.inputTickers.replace(/\s/g, "").toUpperCase().split(',');
    for(let ticker of parsedTickers){ this.savedTickers.push(ticker); }
    this.addTickers.emit(this.savedTickers);
    this.inputTickers = null;
  }
  
  public saveDates(){
    let emittedDates: string[]
    if(this.savedStartDate){ emittedDates.push(dateToString(this.savedStartDate)); }
    if(this.savedEndDate) { emittedDates.push(dateToString(this.savedEndDate)); }
    if(emittedDates.length>0){ this.addDates.emit(emittedDates); }
  }

  public saveInvestment() : void {
    console.log(`saving investment: ${this.inputInvestment}`)
    if(this.inputInvestment){
      this.addInvestment.emit(this.inputInvestment);
    }
  }

  public saveTarget() : void {
    console.log(`saving target: ${this.inputTarget}`)
    if(this.inputTarget){
      this.addTarget.emit(this.inputTarget);
    }
  }

  public saveModel(model : string): void{
    console.log(model)
  }

  public clearInvestment() : void {
    this.inputInvestment = null;
    this.addInvestment.emit(null);
  }

  public clearTarget() : void {
    this.inputTarget = null;
    this.addTarget.emit(null);
  }
}
