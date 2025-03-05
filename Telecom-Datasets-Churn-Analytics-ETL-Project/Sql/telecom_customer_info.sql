SET ANSI_NULLS ON;
GO
SET QUOTED_IDENTIFIER ON;
GO
CREATE TABLE [dbo].[telecom_customer_info](
	[CustomerID] [varchar](50) NOT NULL,
	[Count] [int] NULL,
	[Country] [varchar](100) NULL,
	[State] [varchar](100) NULL,
	[City] [varchar](100) NULL,
	[ZipCode] [varchar](20) NULL,
	[LatLong] [varchar](100) NULL,
	[Latitude] [decimal](10, 6) NULL,
	[Longitude] [decimal](10, 6) NULL,
	[ChurnValue] [int] NULL,
	[ChurnScore] [decimal](5, 2) NULL,
	[CLTV] [decimal](10, 2) NULL,
	[ChurnReason] [varchar](255) NULL,
	[LoadDate] [datetime] NULL
) ON [PRIMARY];
GO
ALTER TABLE [dbo].[telecom_customer_info] ADD CONSTRAINT [PK_telecom_customer_extended] PRIMARY KEY CLUSTERED ([CustomerID] ASC);
GO
CREATE NONCLUSTERED INDEX [IX_customer_extended_churn] ON [dbo].[telecom_customer_info]([ChurnScore] ASC, [ChurnValue] ASC);
GO
CREATE NONCLUSTERED INDEX [IX_customer_extended_location] ON [dbo].[telecom_customer_info]([Country] ASC, [State] ASC, [City] ASC);
GO
ALTER TABLE [dbo].[telecom_customer_info] ADD DEFAULT (getdate()) FOR [LoadDate];
GO
ALTER TABLE [dbo].[telecom_customer_info] ADD CONSTRAINT [FK_customer_extended] FOREIGN KEY([CustomerID]) REFERENCES [dbo].[telecom_analytics]([CustomerID]);
GO