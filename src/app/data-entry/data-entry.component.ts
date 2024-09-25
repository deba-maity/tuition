import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-data-entry',
  templateUrl: './data-entry.component.html',
  styleUrls: ['./data-entry.component.css']
})
export class DataEntryComponent implements OnInit {

  formData: FormGroup<{
    name: FormControl<any>;
    description: FormControl<any>;
    // gender: FormControl<any>;
    contact: FormControl<any>;
    // email: FormControl<any>;
    // password: FormControl<any>;
    // country: FormControl<any>;
    // language: FormControl<any>;
    // skills: FormControl<any>;
    // dob: FormControl<any>

  }>;
  users: any;
  employees: any = [];
  languages: any = [];
  programs: any = [];
  countries: any = [];
  displayedColumns: string[] = ['name', 'description', 'gender', 'contact', 'email', 'password', 'country', 'language'];

  constructor(private http: HttpClient, private formBuilder: FormBuilder, private router: Router) {
    this.formData = this.formBuilder.group({
      name: ['', Validators.required],
      description: ['',],
      // gender: ['', Validators.required],
      // password: ['', Validators.required],
      contact: ['', Validators.required],
      // email: ['', Validators.required,],
      // country: ['', Validators.required],
      // language: ['', Validators.required],
      // skills: ['', Validators.required],
      // dob: ['', Validators.required]
    });



  }

  /**
   * Fetch all employyes data in db
   */
  ngOnInit() {

    this.http.get('http://localhost:3000/employees').subscribe((res: any) => {
      this.employees = res

      // this.getLanguage();
      this.getPrograms();
      this.getCountries()
    })
  }

  /**
   * Function for submit button. Navigation and add user
   */
  onSubmit() {
    this.formData.markAllAsTouched();
    if (this.formData.valid) {
      this.http.post('http://localhost:3000/employees', this.formData.value).subscribe((res: any) => {
        this.employees.push(res)
        this.router.navigate(['/data-list']);
        console.log("testing");

      })
    }
  }

  /**
   * To get language list stored in db.json
   */
  // getLanguage() {
  //   this.http.get('http://localhost:3000/languages').subscribe((res: any) => {
  //     this.languages = res
  //   })
  // }

  /**
   * To get programs list from db
   */
  getPrograms() {
    this.http.get('http://localhost:3000/programs').subscribe((res: any) => {
      this.programs = res
    })
  }

  /**
   * To get countries list from db
   */
  getCountries() {
    this.http.get('http://localhost:3000/countries').subscribe((res: any) => {
      this.countries = res
    })
  }
}
