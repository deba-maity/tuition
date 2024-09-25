import { Component, Input, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css'],
})
export class EditComponent implements OnInit {
  user: any = {}; // Initialize an empty user object

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit() {
    // Get the user ID from the route parameter
    const userId = this.route.snapshot.params['id'];

    // Fetch the user data by ID from your API
    this.http.get(`http://localhost:3000/employees/${userId}`).subscribe((res: any) => {
      this.user = res;
    });
  }

  onSubmit() {
    // Send a PUT request to update the user data in your API
    this.http.put(`http://localhost:3000/employees/${this.user.id}`, this.user).subscribe(() => {
      // After successful update, navigate back to the user list
      this.router.navigate(['/data-list']);
    });
  }
}
