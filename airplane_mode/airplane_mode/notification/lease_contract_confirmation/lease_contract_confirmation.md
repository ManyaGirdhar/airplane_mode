<p>Dear {{ doc.tenant }},</p>

<p>We are pleased to confirm the lease agreement for <strong>{{ doc.shop }}</strong> at <strong>{{ doc.airport }}</strong>. Below are the details of your lease contract:</p>

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%; text-align: left;">
    <tr>
        <td><strong>Shop Name:</strong></td>
        <td>{{ doc.shop }}</td>
    </tr>
    <tr>
        <td><strong>Airport:</strong></td>
        <td>{{ doc.airport }}</td>
    </tr>
    <tr>
        <td><strong>Tenant Name:</strong></td>
        <td>{{ doc.tenant }}</td>
    </tr>
    <tr>
        <td><strong>Lease Start Date:</strong></td>
        <td>{{ doc.start_date }}</td>
    </tr>
    <tr>
        <td><strong>Lease Expiry Date:</strong></td>
        <td>{{ doc.expiry_date }}</td>
    </tr>
    <tr>
        <td><strong>Rent Amount:</strong></td>
        <td>₹{{ doc.rent_amount }} per month</td>
    </tr>
</table>

<p>This contract has been successfully registered, and you may now proceed with further setup and operations. If you have any questions, feel free to contact us.</p>

<p>We look forward to a successful partnership.</p>

<p><strong>Best Regards,</strong><br>
SkyTrack Airport Management System<br>
Email: <a href="mailto:skytrack.management.system@gmail.com">skytrack.management.system@gmail.com</a></p>
